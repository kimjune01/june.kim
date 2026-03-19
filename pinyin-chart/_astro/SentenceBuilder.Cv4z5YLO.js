import{a as x,j as a}from"./AudioService.YDVxfFjf.js";import{r as c}from"./index.WFquGv8Z.js";import{s as f}from"./sentencePatterns.BNl5Va5y.js";import"./preload-helper.Cx_vh1kx.js";function F(){const[n,k]=c.useState(f[0]),[o,w]=c.useState({}),[h,u]=c.useState(!1),[b,j]=c.useState(!1),[r,y]=c.useState(!1),d=["adj-pattern","noun-pattern","verb-pattern","go-pattern","location-pattern","have-pattern","can-pattern","want-pattern","past-pattern"].includes(n.id),p=c.useCallback(()=>{const e=[],i={很:{pinyin:"hěn",english:"very"},是:{pinyin:"shì",english:"is"},不:{pinyin:"bù",english:"not"},不是:{pinyin:"bú shì",english:"is not"},想去:{pinyin:"xiǎng qù",english:"want to go"},不想去:{pinyin:"bù xiǎng qù",english:"don't want to go"},去:{pinyin:"qù",english:"go to"},有多少:{pinyin:"yǒu duōshao",english:"have how many"},为什么:{pinyin:"wèishénme",english:"why"},什么时候:{pinyin:"shénme shíhou",english:"when"},在:{pinyin:"zài",english:"at"},不在:{pinyin:"bú zài",english:"not at"},有:{pinyin:"yǒu",english:"have"},没有:{pinyin:"méiyǒu",english:"don't have"},会:{pinyin:"huì",english:"can"},不会:{pinyin:"bú huì",english:"can't"},想:{pinyin:"xiǎng",english:"want to"},不想:{pinyin:"bù xiǎng",english:"don't want to"},太:{pinyin:"tài",english:"too"},可以:{pinyin:"kěyǐ",english:"may"},怎么这么:{pinyin:"zěnme zhème",english:"how so"},没:{pinyin:"méi",english:"didn't"},了:{pinyin:"le",english:"(completed)"}};for(const g of n.slots){if(g.connector){let t=g.connector;r&&d&&(n.id==="adj-pattern"&&t==="很"?t="不":n.id==="noun-pattern"&&t==="是"?t="不是":n.id==="go-pattern"&&t==="想去"?t="不想去":n.id==="location-pattern"&&t==="在"?t="不在":n.id==="have-pattern"&&t==="有"?t="没有":n.id==="can-pattern"&&t==="会"?t="不会":n.id==="want-pattern"&&t==="想"&&(t="不想"));const s=i[t]||{pinyin:t,english:t};e.push({hanzi:t,pinyin:s.pinyin,english:s.english})}else r&&d&&n.id==="verb-pattern"&&g.id==="verb"?e.push({hanzi:"不",pinyin:"bù",english:"don't"}):r&&d&&n.id==="past-pattern"&&g.id==="verb"&&e.push({hanzi:"没",pinyin:"méi",english:"didn't"});const v=o[g.id];v&&e.push(v)}return n.id==="too-pattern"&&o.adjective&&e.push({hanzi:"了",pinyin:"le",english:"!"}),n.id==="past-pattern"&&o.verb&&!r&&e.push({hanzi:"了",pinyin:"le",english:""}),n.id==="q-permission"&&o.verb&&e.push({hanzi:"吗?",pinyin:"ma",english:"?"}),n.id==="q-did-you"&&o.verb&&e.push({hanzi:"了没有?",pinyin:"le méiyǒu",english:"(or not)?"}),n.id==="q-where"&&o.subject&&e.push({hanzi:"去哪里?",pinyin:"qù nǎlǐ",english:"going where?"}),b&&!["q-permission","q-did-you","q-verb-what","q-who","q-where","q-how-many","q-why","q-when","q-how-so"].includes(n.id)&&e.push({hanzi:"吗?",pinyin:"ma",english:"?"}),e},[n,o,b,r,d])(),m=n.slots.every(e=>o[e.id]),z=c.useCallback(()=>{const e=[];return n.id==="adj-pattern"&&e.push({type:"tip",message:'In Chinese, use 很 (hěn) with adjectives, not 是 (shì). Say "我很高兴", not "我是高兴".'}),r&&n.id==="verb-pattern"&&o.verb?.hanzi==="有"&&e.push({type:"warning",message:'⚠️ 有 (yǒu) is ALWAYS negated with 没有 (méiyǒu), never 不有! Say "我没有钱", not "我不有钱".'}),r&&d&&(n.id==="adj-pattern"?e.push({type:"tip",message:"To negate adjectives, use 不 directly before the adjective. The 很 is removed."}):n.id==="noun-pattern"?e.push({type:"tip",message:'To negate 是, use 不是 (bú shì) meaning "is not".'}):n.id==="verb-pattern"?e.push({type:"tip",message:"To negate most verbs, put 不 before the verb. Exception: 有 uses 没有."}):n.id==="go-pattern"?e.push({type:"tip",message:`不想去 means "don't want to go". 不 negates 想, not 去.`}):n.id==="location-pattern"?e.push({type:"tip",message:`不在 means "not at" or "not present". Use this to say someone isn't somewhere.`}):n.id==="have-pattern"?e.push({type:"correct",message:"有 is ALWAYS negated with 没有 (méiyǒu), never 不有. This is automatic!"}):n.id==="can-pattern"?e.push({type:"tip",message:`不会 means "can't" or "don't know how to". It negates learned abilities.`}):n.id==="want-pattern"?e.push({type:"tip",message:`不想 means "don't want to". Use this to politely decline or express disinterest.`}):n.id==="past-pattern"&&e.push({type:"correct",message:"Past tense negation uses 没 (méi), NOT 不. And there's no 了 in negative past!"})),n.id==="have-pattern"&&!r&&e.push({type:"tip",message:"有 (yǒu) expresses possession. Remember: negate with 没有, never 不有!"}),n.id==="can-pattern"&&!r&&e.push({type:"tip",message:"会 (huì) indicates learned skills or abilities. For physical ability, use 能 (néng)."}),n.id==="too-pattern"&&e.push({type:"tip",message:'太...了 is an emphatic pattern. It can express "too much" or strong emotion (太好了 = Great!).'}),n.id==="past-pattern"&&!r&&e.push({type:"tip",message:"了 (le) after the verb indicates a completed action. Negate with 没 (no 了 needed)."}),b&&e.push({type:"tip",message:"Adding 吗 turns any statement into a yes/no question. The word order stays the same!"}),e},[n,o,b,r,d])(),N=c.useCallback(async()=>{if(!(!m||h)){u(!0);try{const e=p.map(i=>i.hanzi).join("");await x.playVocabulary(e,!0)}catch(e){console.error("Error playing sentence:",e)}finally{u(!1)}}},[m,h,p]),q=c.useCallback(async()=>{if(!(!m||h)){u(!0);try{for(const e of p)await x.playVocabulary(e.hanzi,!0),await new Promise(i=>setTimeout(i,300))}catch(e){console.error("Error playing syllables:",e)}finally{u(!1)}}},[m,h,p]),S=c.useCallback(async e=>{try{await x.playVocabulary(e.hanzi,!0)}catch(i){console.error("Error playing word:",i)}},[]),C=e=>{const i=f.find(l=>l.id===e);i&&(k(i),w({}),y(!1),j(!1),u(!1))},P=(e,i)=>{w(l=>({...l,[e]:i}))};return a.jsxs("div",{className:"sentence-builder",children:[a.jsxs("div",{className:"pattern-section",children:[a.jsx("label",{className:"section-label",children:"Choose a pattern:"}),a.jsxs("select",{className:"pattern-select",value:n.id,onChange:e=>C(e.target.value),children:[a.jsx("optgroup",{label:"Statements",children:f.filter(e=>e.category==="statement").map(e=>a.jsxs("option",{value:e.id,children:[e.name," (",e.example.english,")"]},e.id))}),a.jsx("optgroup",{label:"Questions",children:f.filter(e=>e.category==="question").map(e=>a.jsxs("option",{value:e.id,children:[e.name," (",e.example.english,")"]},e.id))})]}),a.jsx("p",{className:"pattern-description",children:n.description})]}),a.jsxs("div",{className:"example-section",children:[a.jsx("span",{className:"example-label",children:"Example:"}),a.jsx("span",{className:"example-chinese",children:n.example.chinese}),a.jsx("span",{className:"example-pinyin",children:n.example.pinyin}),a.jsx("span",{className:"example-english",children:n.example.english})]}),a.jsxs("div",{className:"slots-section",children:[n.slots.map((e,i)=>{const l=d&&(n.id==="verb-pattern"&&e.id==="verb"||n.id==="past-pattern"&&e.id==="verb"||n.id==="adj-pattern"&&e.connector==="很"||n.id==="noun-pattern"&&e.connector==="是"||n.id==="go-pattern"&&e.connector==="想去"||n.id==="location-pattern"&&e.connector==="在"||n.id==="have-pattern"&&e.connector==="有"||n.id==="can-pattern"&&e.connector==="会"||n.id==="want-pattern"&&e.connector==="想"),g={很:"hěn",是:"shì",不:"bù",不是:"bú shì",想去:"xiǎng qù",不想去:"bù xiǎng qù",在:"zài",不在:"bú zài",有:"yǒu",没有:"méiyǒu",会:"huì",不会:"bú huì",想:"xiǎng",不想:"bù xiǎng",太:"tài",去:"qù",有多少:"yǒu duōshao",为什么:"wèishénme",什么时候:"shénme shíhou",可以:"kěyǐ",怎么这么:"zěnme zhème",没:"méi"},t=(()=>{if(!e.connector)return null;let s=e.connector;return r&&d&&(n.id==="adj-pattern"&&e.connector==="很"?s="不":n.id==="noun-pattern"&&e.connector==="是"?s="不是":n.id==="go-pattern"&&e.connector==="想去"?s="不想去":n.id==="location-pattern"&&e.connector==="在"?s="不在":n.id==="have-pattern"&&e.connector==="有"?s="没有":n.id==="can-pattern"&&e.connector==="会"?s="不会":n.id==="want-pattern"&&e.connector==="想"&&(s="不想")),{hanzi:s,pinyin:g[s]||""}})();return a.jsxs("div",{className:"slot-group",children:[l&&n.id==="verb-pattern"&&a.jsxs("div",{className:`negation-toggle inline ${r?"active":""}`,onClick:()=>y(!r),children:[a.jsx("span",{className:"connector-hanzi",children:"不"}),a.jsx("span",{className:"connector-pinyin",children:"bù"})]}),l&&n.id==="past-pattern"&&a.jsxs("div",{className:`negation-toggle inline ${r?"active":""}`,onClick:()=>y(!r),children:[a.jsx("span",{className:"connector-hanzi",children:"没"}),a.jsx("span",{className:"connector-pinyin",children:"méi"})]}),e.connector&&a.jsxs("div",{className:`connector ${l?"toggleable":""} ${r&&l?"negated":""}`,onClick:l?()=>y(!r):void 0,children:[a.jsx("span",{className:"connector-hanzi",children:t?.hanzi}),a.jsx("span",{className:"connector-pinyin",children:t?.pinyin})]}),a.jsxs("div",{className:"slot",children:[a.jsx("label",{className:"slot-label",children:e.label}),a.jsx("div",{className:"word-grid",children:e.words.map(s=>a.jsxs("button",{className:`word-btn ${o[e.id]?.hanzi===s.hanzi?"selected":""}`,onClick:()=>{P(e.id,s),S(s)},children:[a.jsx("span",{className:"word-hanzi",children:s.hanzi}),a.jsx("span",{className:"word-pinyin",children:s.pinyin}),a.jsx("span",{className:"word-english",children:s.english})]},s.hanzi))})]})]},e.id)}),n.category==="statement"&&a.jsx("div",{className:"question-toggle",children:a.jsxs("label",{className:"toggle-label",children:[a.jsx("input",{type:"checkbox",checked:b,onChange:e=>j(e.target.checked)}),a.jsx("span",{className:"toggle-switch"}),a.jsxs("span",{className:"toggle-text",children:[a.jsx("span",{className:"toggle-hanzi",children:"吗?"}),a.jsx("span",{className:"toggle-pinyin",children:"ma"})]})]})})]}),a.jsxs("div",{className:`result-section ${m?"complete":""}`,children:[a.jsx("div",{className:"result-sentence",children:p.length>0?a.jsxs(a.Fragment,{children:[a.jsx("div",{className:"result-hanzi",children:p.map((e,i)=>a.jsx("span",{className:"result-part",children:e.hanzi},i))}),a.jsx("div",{className:"result-pinyin",children:p.map((e,i)=>a.jsx("span",{className:"result-part",children:e.pinyin},i))}),a.jsx("div",{className:"result-english",children:p.map((e,i)=>a.jsx("span",{className:"result-part",children:e.english},i))})]}):a.jsx("span",{className:"result-placeholder",children:"Select words to build a sentence..."})}),m&&a.jsxs("div",{className:"play-buttons",children:[a.jsx("button",{className:"play-btn play-syllables-btn",onClick:q,disabled:h,children:"▶ Syllables"}),a.jsx("button",{className:"play-btn play-sentence-btn",onClick:N,disabled:h,children:"▶ Sentence"})]})]}),z.length>0&&a.jsx("div",{className:"grammar-feedback",children:z.map((e,i)=>a.jsx("div",{className:`feedback-item feedback-${e.type}`,children:e.message},i))}),a.jsx("style",{children:`
        .sentence-builder {
          max-width: 800px;
          margin: 0 auto;
        }

        .pattern-section {
          margin-bottom: var(--spacing-xl);
        }

        .section-label {
          display: block;
          font-weight: var(--font-weight-medium);
          margin-bottom: var(--spacing-sm);
          color: var(--color-text);
        }

        .pattern-select {
          width: 100%;
          padding: var(--spacing-sm) var(--spacing-md);
          font-size: var(--font-size-base);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          background: var(--color-surface);
          color: var(--color-text);
          cursor: pointer;
        }

        .pattern-select:focus {
          outline: none;
          border-color: var(--color-primary);
        }

        .pattern-description {
          margin-top: var(--spacing-sm);
          font-size: var(--font-size-sm);
          color: var(--color-text-secondary);
        }

        .example-section {
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          gap: var(--spacing-md);
          padding: var(--spacing-md);
          background: var(--color-surface);
          border-radius: var(--radius-md);
          margin-bottom: var(--spacing-xl);
        }

        .example-label {
          font-size: var(--font-size-sm);
          color: var(--color-text-secondary);
        }

        .example-chinese {
          font-size: var(--font-size-xl);
          font-weight: var(--font-weight-semibold);
        }

        .example-pinyin {
          color: var(--color-primary);
        }

        .example-english {
          color: var(--color-text-secondary);
        }

        .slots-section {
          display: flex;
          flex-wrap: wrap;
          gap: var(--spacing-lg);
          align-items: flex-start;
          margin-bottom: var(--spacing-xl);
        }

        .slot-group {
          display: flex;
          flex-direction: column;
          gap: var(--spacing-sm);
        }

        .connector {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-md);
          padding: var(--spacing-md) var(--spacing-lg);
          background: rgba(74, 144, 226, 0.1);
          border-radius: var(--radius-lg);
          width: 100%;
        }

        .question-toggle {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-md);
          padding: var(--spacing-md) var(--spacing-lg);
          background: rgba(74, 144, 226, 0.1);
          border-radius: var(--radius-lg);
          width: 100%;
          cursor: pointer;
          transition: opacity 0.2s ease;
        }

        .question-toggle:has(input:not(:checked)) {
          opacity: 0.4;
        }

        /* Inline negation toggle for verb-pattern */
        .negation-toggle.inline {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-md);
          padding: var(--spacing-md) var(--spacing-lg);
          background: var(--color-border);
          border-radius: var(--radius-lg);
          width: 100%;
          cursor: pointer;
          transition: all 0.2s ease;
          opacity: 0.4;
        }

        .negation-toggle.inline:hover {
          opacity: 0.7;
        }

        .negation-toggle.inline.active {
          opacity: 1;
          background: rgba(220, 53, 69, 0.15);
        }

        /* Toggleable connectors */
        .connector.toggleable {
          cursor: pointer;
          transition: all 0.2s ease;
          border: 2px dashed transparent;
        }

        .connector.toggleable:hover {
          border-color: var(--color-primary);
        }

        .connector.toggleable.negated {
          background: rgba(220, 53, 69, 0.15);
          border: 2px solid rgba(220, 53, 69, 0.3);
        }

        .toggle-label {
          display: flex;
          align-items: center;
          gap: var(--spacing-md);
          cursor: pointer;
        }

        .toggle-label input {
          display: none;
        }

        .toggle-switch {
          width: 48px;
          height: 26px;
          background: var(--color-border);
          border-radius: 13px;
          position: relative;
          transition: background 0.2s ease;
          flex-shrink: 0;
        }

        .toggle-switch::after {
          content: '';
          position: absolute;
          top: 3px;
          left: 3px;
          width: 20px;
          height: 20px;
          background: white;
          border-radius: 50%;
          transition: transform 0.2s ease;
        }

        .toggle-label input:checked + .toggle-switch {
          background: var(--color-primary);
        }

        .toggle-label input:checked + .toggle-switch::after {
          transform: translateX(22px);
        }

        .toggle-text {
          display: flex;
          align-items: center;
          gap: var(--spacing-md);
        }

        .toggle-hanzi {
          font-size: 4rem;
          font-weight: 300;
          color: var(--color-text);
        }

        .toggle-pinyin {
          font-size: var(--font-size-base);
          color: var(--color-text-secondary);
        }

        .connector-hanzi {
          font-size: 4rem;
          font-weight: 300;
          color: var(--color-text);
        }

        .connector-pinyin {
          font-size: var(--font-size-base);
          color: var(--color-text-secondary);
        }

        .slot {
          flex: 1;
          min-width: 200px;
        }

        .slot-label {
          display: block;
          font-size: var(--font-size-sm);
          font-weight: var(--font-weight-medium);
          color: var(--color-text-secondary);
          margin-bottom: var(--spacing-sm);
        }

        .word-grid {
          display: flex;
          flex-wrap: wrap;
          gap: var(--spacing-xs);
        }

        .word-btn {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: var(--spacing-sm);
          background: var(--color-surface);
          border: 2px solid var(--color-border);
          border-radius: var(--radius-md);
          cursor: pointer;
          transition: all var(--transition-fast);
          min-width: 70px;
        }

        .word-btn:hover {
          border-color: var(--color-primary);
        }

        .word-btn.selected {
          border-color: var(--color-primary);
          background: rgba(74, 144, 226, 0.1);
        }

        .word-hanzi {
          font-size: var(--font-size-lg);
          font-weight: var(--font-weight-semibold);
        }

        .word-pinyin {
          font-size: var(--font-size-xs);
          color: var(--color-primary);
        }

        .word-english {
          font-size: var(--font-size-xs);
          color: var(--color-text-secondary);
        }

        .result-section {
          padding: var(--spacing-xl);
          background: var(--color-surface);
          border: 2px dashed var(--color-border);
          border-radius: var(--radius-lg);
          text-align: center;
          margin-bottom: var(--spacing-lg);
        }

        .result-section.complete {
          border-style: solid;
          border-color: var(--color-primary);
          background: rgba(74, 144, 226, 0.05);
        }

        .result-sentence {
          margin-bottom: var(--spacing-md);
        }

        .result-hanzi {
          font-size: var(--font-size-3xl);
          font-weight: var(--font-weight-semibold);
          margin-bottom: var(--spacing-sm);
        }

        .result-pinyin {
          font-size: var(--font-size-lg);
          color: var(--color-primary);
          margin-bottom: var(--spacing-xs);
        }

        .result-english {
          font-size: var(--font-size-base);
          color: var(--color-text-secondary);
        }

        .result-part {
          margin: 0 2px;
        }

        .result-placeholder {
          color: var(--color-text-secondary);
          font-style: italic;
        }

        .play-buttons {
          display: flex;
          gap: var(--spacing-sm);
          justify-content: center;
        }

        .play-btn {
          padding: var(--spacing-md) var(--spacing-lg);
          color: white;
          border: none;
          border-radius: var(--radius-lg);
          font-size: var(--font-size-base);
          font-weight: var(--font-weight-semibold);
          cursor: pointer;
          transition: all var(--transition-fast);
        }

        .play-syllables-btn {
          background: var(--color-text-secondary);
        }

        .play-sentence-btn {
          background: var(--color-primary);
        }

        .play-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          filter: brightness(1.1);
        }

        .play-btn:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .grammar-feedback {
          display: flex;
          flex-direction: column;
          gap: var(--spacing-sm);
        }

        .feedback-item {
          padding: var(--spacing-md);
          border-radius: var(--radius-md);
          font-size: var(--font-size-sm);
          color: var(--color-text);
        }

        .feedback-tip {
          background: rgba(74, 144, 226, 0.1);
          border-left: 4px solid var(--color-primary);
        }

        .feedback-warning {
          background: rgba(220, 53, 69, 0.1);
          border-left: 4px solid #dc3545;
          font-weight: var(--font-weight-medium);
        }

        .feedback-correct {
          background: rgba(40, 167, 69, 0.1);
          border-left: 4px solid #28a745;
        }

        @media (max-width: 600px) {
          .slots-section {
            flex-direction: column;
          }

          .slot-group {
            width: 100%;
            flex-direction: column;
          }

          .connector {
            padding-top: 0;
            justify-content: center;
          }

          .slot {
            width: 100%;
          }

          .result-hanzi {
            font-size: var(--font-size-2xl);
          }
        }
      `})]})}export{F as default};
