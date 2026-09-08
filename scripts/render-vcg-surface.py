# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib==3.10.8", "numpy>=2,<3"]
# ///
"""Render the reported-value upper envelope. Run with uv run this-file.py."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, LightSource
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11, 'svg.fonttype':'none', 'pdf.fonttype':42})
# The exponent deliberately has no 1/2, matching reportedVal in the paper.
reports = [(-1.45, -.6, .72, 3.4), (-.15, .8, 2.5, 1.35), (1.65, -.3, 1.12, 2.35)]
colors = ['#3767A6', '#128C87', '#D07551']
def values(x, y):
    return np.array([b*np.exp(-((x-cx)**2+(y-cy)**2)/s**2) for cx,cy,s,b in reports])
# Check the geometric controls before rendering.
for i,(cx,cy,s,b) in enumerate(reports):
    assert np.isclose(values(cx,cy)[i], b)
    assert np.isclose(values(cx+s,cy)[i], b/np.e)
x=np.linspace(-3.6,3.8,150); y=np.linspace(-2.7,3.,125)
X,Y=np.meshgrid(x,y); V=values(X,Y); Z=V.max(axis=0); W=V.argmax(axis=0)
fig=plt.figure(figsize=(7.2,4.6), facecolor='#FAFAF7')
ax=fig.add_axes([.10,.075,.87,.92], projection='3d', computed_zorder=False, facecolor='#FAFAF7')
ax.set_proj_type('ortho'); ax.view_init(elev=34, azim=-63)
ax.set_box_aspect((7.4,5.7,3.6)); ax.set(xlim=(-3.6,3.8),ylim=(-2.7,3),zlim=(0,3.8))
ax.set_xlabel(r'Embedding $x_1$', labelpad=7, fontsize=11)
ax.set_ylabel(r'Embedding $x_2$', labelpad=7, fontsize=11)
ax.set_zlabel('Reported value', labelpad=5, fontsize=11, color='#53646b')
ax.set_xticks([-3,0,3]); ax.set_yticks([-2,0,2]); ax.set_zticks([0,1,2,3])
ax.zaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:g}'))
ax.tick_params(labelsize=10, colors='#555555', pad=2)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.fill=False
    axis.pane.set_edgecolor('#d2d8d8')
    axis.line.set_color('#888888')
    axis._axinfo['grid'].update(color='#d9dddd', linestyle='-', linewidth=.4)
ax.zaxis._axinfo['juggled']=(1,2,0)
# Split mesh faces at report intersections instead of assigning one color
# to a whole rectangular face. This keeps color boundaries off the grid.
def score(i, point):
    cx,cy,s,b=reports[i]
    return np.log(b)-((point[0]-cx)**2+(point[1]-cy)**2)/s**2

def clip(poly, i, j):
    result=[]
    for a,b in zip(poly, poly[1:]+poly[:1]):
        da=score(i,a)-score(j,a); db=score(i,b)-score(j,b)
        if da>=0:
            result.append(a)
        if (da>=0)!=(db>=0):
            lo,hi=0.,1.
            for _ in range(40):
                mid=(lo+hi)/2
                point=a+mid*(b-a)
                if ((score(i,point)-score(j,point))>=0)==(da>=0):
                    lo=mid
                else:
                    hi=mid
            crossing=a+(lo+hi)/2*(b-a)
            assert abs(score(i,crossing)-score(j,crossing))<1e-8
            result.append(crossing)
    return result

faces=[]; facecolors=[]
gx=np.linspace(-3.6,3.8,29); gy=np.linspace(-2.7,3.,25)
for left,right in zip(gx[:-1],gx[1:]):
    for bottom,top in zip(gy[:-1],gy[1:]):
        corners=[np.array(v) for v in [(left,bottom),(right,bottom),(right,top),(left,top)]]
        for i,(cx,cy,s,bid) in enumerate(reports):
            poly=corners.copy()
            for j in range(len(reports)):
                if j!=i and poly:
                    poly=clip(poly,i,j)
            if len(poly)<3:
                continue
            pts=np.array(poly)
            heights=values(pts[:,0],pts[:,1])[i]
            faces.append(np.column_stack((pts,heights)))
            mid=pts.mean(axis=0); h=values(*mid)[i]
            normal=np.array([2*(mid[0]-cx)*h/s**2,2*(mid[1]-cy)*h/s**2,1.])
            normal/=np.linalg.norm(normal)
            light=np.array([-.4,-.5,.76]); light/=np.linalg.norm(light)
            shade=max(0.,normal@light)
            facecolors.append(np.array(to_rgb(colors[i]))*(.6+.4*shade)*.26+.74)
surf=Poly3DCollection(faces,facecolors=facecolors,edgecolors=(.14,.26,.32,.45),linewidths=.4,zorder=3)
ax.add_collection3d(surf)
t=np.linspace(0,2*np.pi,240)
for i,(cx,cy,s,b) in enumerate(reports):
    # Floor contours show individual reports, including portions below the envelope.
    for fraction in (.25,.6):
        r=s*np.sqrt(-np.log(fraction))
        ax.plot(cx+r*np.cos(t),cy+r*np.sin(t),np.full_like(t,0.),color=colors[i],lw=.8,alpha=.7,zorder=2)
    # Sparse level curves are drawn only where this advertiser wins.
    for fraction in ():
        r=s*np.sqrt(-np.log(fraction)); xx=cx+r*np.cos(t); yy=cy+r*np.sin(t)
        zz=np.full_like(t,b*fraction+.007)
        zz[values(xx,yy).argmax(axis=0)!=i]=np.nan
        ax.plot(xx,yy,zz,color=colors[i],lw=.65,alpha=.7,zorder=4)
    ax.text(cx,cy,b+.22,chr(65+i),color=colors[i],ha='center',fontsize=12,fontweight='bold',zorder=7)
# Floor frame and center indicator.
ax.plot([-3.6,3.8,3.8,-3.6,-3.6],[-2.7,-2.7,3,3,-2.7],[0.]*5,color='#c7c7c7',lw=.7,zorder=1)
cx,cy,s,b=reports[0]
ax.scatter([cx],[cy],[0.],color=colors[0],s=9,alpha=.65,zorder=6)
ax.plot([cx,cx],[cy,cy],[0.,b],color=colors[0],lw=.55,alpha=.55,ls=(0,(3,4)),zorder=5)
ax.plot([cx,cx+s],[cy,cy],[0.,0.],color=colors[0],lw=.65,alpha=.65,zorder=6)
fig.canvas.draw()
def callout(label, xyz, xytext):
    px,py,_=proj3d.proj_transform(*xyz,ax.get_proj())
    ax.annotate(label,xy=(px,py),xycoords='data',xytext=xytext,textcoords='figure fraction',fontsize=10,color='#68767c',ha='left',va='center',arrowprops={'arrowstyle':'-','color':'#9da7ab','lw':.5},zorder=10)
callout('bid  $b$',(cx,cy,b),(.075,.79))
callout('center  $c$',(cx,cy,0.),(.25,.12))
callout('reach  $\\sigma$',(cx+s*.7,cy,0.),(.08,.23))


out=ROOT/'tmp/pdfs/vcg-surface'; out.mkdir(parents=True,exist_ok=True)
for ext in ['svg','pdf','png']:
    fig.savefig(out/f'vcg-fig1.{ext}',dpi=180,pad_inches=.08)

svg=out/'vcg-fig1.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
