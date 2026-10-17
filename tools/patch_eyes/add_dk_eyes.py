#!/usr/bin/env python3
"""Add Death-Knight eye glow (geoset 1703) to a WotLK (v264) M2 + skin, modelled on the Dark Iron Dwarf:
  1. the eyeball submesh is duplicated (130 new vertices pushed OFFSET along their normals) and drawn right after
     the normal eye batch with a DK eye texture                                   -> blue eyes
  2. an additive halo (2 x 3 concentric rings, bound to the two eye bones) drawn after that, textured with the
     cyan alpha-ramp patch of the Dark Iron Dwarf glow BLP                         -> glow around the eyes
Both batches use geoset 1703, which the client only switches on for Death Knights.
Re-uses unused texture slots (default 5 and 6) so the texture array does not have to move.
usage: add_dk_eyes.py in.m2 in.skin out.m2 out.skin DK_EYE_BLP [HALO_BLP|none] [eye_slot=9] [dk_slot=5] [halo_slot=6] [offset=0.0015] [halo_mat=9]
(always run it on the M2/skin from BEFORE this step, not on its own output)"""
import struct, sys, math
a = sys.argv
m2p, skp, m2o, sko, dkpath = a[1:6]
halopath = a[6] if len(a) > 6 else 'Character\\highmountaintauren\\male\\highmountaintaurenmale_eyeglow.blp'
if halopath.lower() == 'none': halopath = None
EYE_SLOT=int(a[7]) if len(a)>7 else 9; DK_SLOT=int(a[8]) if len(a)>8 else 5; HALO_SLOT=int(a[9]) if len(a)>9 else 6
OFFSET=float(a[10]) if len(a)>10 else 0.0015; HALO_MAT=int(a[11]) if len(a)>11 else 9
DK_SID = 1703
m = bytearray(open(m2p,'rb').read()); s = open(skp,'rb').read()
assert m[:4]==b'MD20' and struct.unpack_from('<I',m,4)[0]==264
M=lambda f,o:struct.unpack_from(f,m,o)
nv,ov = M('<II',0x3c); tn,to = M('<II',0x50); tln,tlo = M('<II',0x80); mn,mo = M('<II',0x70)
tl = list(struct.unpack_from('<%dH'%tln,m,tlo)); mats=[M('<HH',mo+i*4) for i in range(mn)]
_,ni,oi,nt,ot,np_,op,ns,os_,nx,ox,bmax = struct.unpack_from('<4sIIIIIIIIIII',s,0)
lookup=list(struct.unpack_from('<%dH'%ni,s,oi)); tri=list(struct.unpack_from('<%dH'%nt,s,ot))
props=[s[op+i*4:op+i*4+4] for i in range(np_)]
subs=[bytearray(s[os_+i*48:os_+i*48+48]) for i in range(ns)]
bats=[bytearray(s[ox+i*24:ox+i*24+24]) for i in range(nx)]
rd=lambda b,o:struct.unpack_from('<H',b,o)[0]
def free_slot(slot):
    cs=[c for c,t in enumerate(tl) if t==slot]; assert cs,'no texture-lookup entry for slot %d'%slot
    for b in bats:
        cnt=rd(b,14); combo=rd(b,16)
        assert not any(tl[combo+k]==slot for k in range(cnt)),'slot %d already used by a batch'%slot
    assert M('<I',to+slot*16)[0]==0,'slot %d is not a file texture'%slot
    return cs[0]
assert not any(rd(b,0)==DK_SID for b in subs),'geoset %d already present - run on the un-patched files'%DK_SID
DK_COMBO=free_slot(DK_SLOT); HALO_COMBO=free_slot(HALO_SLOT) if halopath else None
if halopath: assert mats[HALO_MAT]==(0x15,4),'material %d is not additive (0x15, blend 4): %s'%(HALO_MAT,mats[HALO_MAT])
eye_bi=[i for i,b in enumerate(bats) if tl[rd(b,16)]==EYE_SLOT]; assert len(eye_bi)==1,'expected one eye batch: %s'%eye_bi
eye_bi=eye_bi[0]; sec=rd(bats[eye_bi],4)
sid,lvl,vs,vc,is_,ic = struct.unpack_from('<HHHHHH',subs[sec],0); st=(lvl<<16)|is_
print('eye batch',eye_bi,'-> submesh',sec,'verts',vc,'idx',ic)
vert=lambda k: m[ov+lookup[k]*48: ov+lookup[k]*48+48]
# ---------- 1. DK eye duplicate
newv=bytearray()
for k in range(vs,vs+vc):
    v=bytearray(vert(k)); px,py,pz=struct.unpack_from('<3f',v,0); nx_,ny,nz=struct.unpack_from('<3f',v,20)
    L=math.sqrt(nx_*nx_+ny*ny+nz*nz) or 1.0
    struct.pack_into('<3f',v,0,px+OFFSET*nx_/L,py+OFFSET*ny/L,pz+OFFSET*nz/L); newv+=v
dk_base=nv; n_dk=vc
# ---------- 2. halo
halo_v=bytearray(); halo_tri=[]; halo_props=[]
if halopath:
    N=12; RING=[(0.88,0.070),(1.50,0.040),(2.20,0.012)]      # (radius / eye radius, V on the glow patch)
    for sign in (1,-1):
        ks=[k for k in range(vs,vs+vc) if sign*struct.unpack_from('<3f',vert(k),0)[1]>0]
        pts=[struct.unpack_from('<3f',vert(k),0) for k in ks]
        cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts); cz=sum(p[2] for p in pts)/len(pts)
        re=max(math.hypot(p[1]-cy,p[2]-cz) for p in pts); fx=max(p[0] for p in pts)+0.006
        ref=vert(ks[0]); wts=bytes(ref[12:16]); bon=bytes(ref[16:20]); pr=props[ks[0]]
        assert len(set(bytes(vert(k)[16:20]) for k in ks))==1, 'eye has more than one bone'
        first=len(halo_v)//48
        for (rm,V) in RING:
            for i in range(N):
                ang=2*math.pi*i/N; v=bytearray(48)
                struct.pack_into('<3f',v,0,fx,cy+rm*re*math.cos(ang),cz+rm*re*math.sin(ang))
                v[12:16]=wts; v[16:20]=bon; struct.pack_into('<3f',v,20,1.0,0.0,0.0)
                struct.pack_into('<2f',v,32,0.08,V); struct.pack_into('<2f',v,40,0.08,V)
                halo_v+=v; halo_props.append(pr)
        for band in range(len(RING)-1):
            for i in range(N):
                j=(i+1)%N; p=first+band*N; q=first+(band+1)*N
                halo_tri+=[p+i,p+j,q+i, p+j,q+j,q+i]
    halo_base=nv+n_dk
n_halo=len(halo_v)//48
assert nv+n_dk+n_halo<=65535
# ---------- relocate vertex array (once) and append
arr=bytes(m[ov:ov+nv*48])+bytes(newv)+bytes(halo_v)
while len(m)%16: m+=b'\0'
new_ov=len(m); m+=arr; struct.pack_into('<II',m,0x3c,nv+n_dk+n_halo,new_ov)
def set_tex(slot,path):
    rec=to+slot*16; t,fl,ln,off=struct.unpack_from('<IIII',m,rec); nm=path.encode()+b'\0'; o=len(m); m.extend(nm)
    struct.pack_into('<IIII',m,rec,0,fl,len(nm),o)
set_tex(DK_SLOT,dkpath)
if halopath: set_tex(HALO_SLOT,halopath)
# ---------- skin: DK eye submesh + batch
new_vs=len(lookup); new_is=len(tri); assert new_is<65536
lookup+=[dk_base+i for i in range(vc)]; props+=props[vs:vs+vc]; tri+=[t_-vs+new_vs for t_ in tri[st:st+ic]]
sb=bytearray(subs[sec]); struct.pack_into('<HHHHHH',sb,0,DK_SID,new_is>>16,new_vs,vc,new_is&0xFFFF,ic); subs.append(sb)
bb=bytearray(bats[eye_bi]); k=len(subs)-1
struct.pack_into('<H',bb,4,k); struct.pack_into('<H',bb,6,k); struct.pack_into('<H',bb,16,DK_COMBO); bats.insert(eye_bi+1,bb); at=eye_bi+2
# ---------- skin: halo submesh + batch
if halopath:
    new_vs=len(lookup); new_is=len(tri); assert new_is<65536 and new_vs+n_halo<65536
    lookup+=[halo_base+i for i in range(n_halo)]; props+=halo_props; tri+=[new_vs+t_ for t_ in halo_tri]
    hb=bytearray(subs[sec]); struct.pack_into('<HHHHHH',hb,0,DK_SID,new_is>>16,new_vs,n_halo,new_is&0xFFFF,len(halo_tri)); subs.append(hb)
    hbat=bytearray(bats[eye_bi]); k=len(subs)-1
    struct.pack_into('<H',hbat,4,k); struct.pack_into('<H',hbat,6,k); struct.pack_into('<H',hbat,10,HALO_MAT); struct.pack_into('<H',hbat,16,HALO_COMBO)
    bats.insert(at,hbat)
# ---------- write skin
pad=lambda n:(-n)%4
out=bytearray(48)
oi2=len(out); out+=struct.pack('<%dH'%len(lookup),*lookup); out+=b'\0'*pad(len(out))
ot2=len(out); out+=struct.pack('<%dH'%len(tri),*tri); out+=b'\0'*pad(len(out))
op2=len(out); out+=b''.join(props)
os2=len(out); out+=b''.join(bytes(x) for x in subs)
ox2=len(out); out+=b''.join(bytes(x) for x in bats)
struct.pack_into('<4sIIIIIIIIIII',out,0,b'SKIN',len(lookup),oi2,len(tri),ot2,len(props),op2,len(subs),os2,len(bats),ox2,bmax)
open(m2o,'wb').write(m); open(sko,'wb').write(out)
print('DK eye overlay: %d vertices, %d indices | halo: %d vertices, %d indices | skin now %d indices, %d submeshes'%(n_dk,ic,n_halo,len(halo_tri),len(tri),len(subs)))