import{j as i}from"./jsx-runtime.CLpGMVip.js";import{r as a}from"./index.B9mnsnPE.js";import{i as g,g as b,a as f}from"./spectrum.rSbPmbmO.js";import{p as m,l as h}from"./util.C4W5Av6k.js";import{u as x}from"./useClient.CropWvdz.js";import"./_commonjsHelpers.BosuxZz1.js";import"./index.CfqHpm9h.js";import"./index.pm4xYsgm.js";import"./preload-helper.DsSmCdsn.js";import"./index.BE2LGbB0.js";/* empty css                      */let l,d,u;typeof window<"u"&&(l=m(),d=h(),u=g());function y({sound:o="bd",label:r}){const[n,t]=a.useState(!1),e=a.useRef(!1),c=a.useCallback(async()=>{e.current||(await Promise.all([d,l,u]),e.current=!0),t(!0);try{const p=b().currentTime+.01;await f({s:o},p,1)}catch(s){console.error("Soundboard error:",s)}setTimeout(()=>t(!1),150)},[o]);return x()?i.jsx("button",{onClick:c,className:`
        px-6 py-4
        rounded-lg
        font-mono text-lg
        border-2 border-lineHighlight
        bg-background
        hover:bg-lineHighlight
        active:scale-95
        transition-all duration-100
        cursor-pointer
        ${n?"bg-lineHighlight scale-95":""}
      `,children:r||o}):i.jsx("button",{disabled:!0,children:r||o})}function T({sounds:o}){return i.jsx("div",{className:"flex flex-wrap gap-2 p-4 bg-background rounded-lg border border-lineHighlight",children:o.map((r,n)=>{const t=typeof r=="string"?r:r.sound,e=typeof r=="string"?r:r.label;return i.jsx(y,{sound:t,label:e},n)})})}export{y as Soundboard,T as SoundboardGrid};
