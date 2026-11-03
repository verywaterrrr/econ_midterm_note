const progressKey='econ2103-checklist-v2';
function load(){try{const value=JSON.parse(localStorage.getItem(progressKey)||'{}');return value&&typeof value==='object'?value:{}}catch{return {}}}
function save(data){try{localStorage.setItem(progressKey,JSON.stringify(data))}catch{}}
function updateProgress(){
 const data=load(),items=data.items||{};
 document.querySelectorAll('[data-item-link]').forEach(a=>{a.classList.toggle('reviewed',!!items[a.dataset.itemLink]?.reviewed)});
 document.querySelectorAll('[data-chapter-progress]').forEach(el=>{const chapter=el.dataset.chapterProgress;const done=Object.entries(items).filter(([k,v])=>k.startsWith(chapter+'-')&&v.reviewed).length;const total={1:10,2:12,3:8,4:10,5:11,6:12,7:10,8:13,14:12,15:14,cross:5}[chapter];el.textContent=done+' / '+total+' reviewed · 已複習'});
 const total=document.querySelector('[data-total-progress]');if(total)total.textContent=Object.values(items).filter(x=>x.reviewed).length+' / 117 items reviewed · 本機紀錄';
}
const current=document.querySelector('[data-current-item]');
if(current){const data=load();data.last=current.dataset.currentPath;save(data)}
const resume=document.querySelector('[data-resume]');
if(resume){const last=load().last;if(typeof last==='string'&&/^lessons\/ch(?:\d+|cross)-\d{2}\.html$/.test(last)){resume.href=last;resume.textContent='Continue learning 繼續學習 ↗'}}
document.querySelectorAll('[data-reviewed]').forEach(input=>{
 input.checked=!!load().items?.[input.dataset.reviewed]?.reviewed;
 input.addEventListener('change',()=>{const data=load();data.items??={};data.items[input.dataset.reviewed]={...data.items[input.dataset.reviewed],reviewed:input.checked};save(data);updateProgress()})
});
document.querySelectorAll('.question').forEach(question=>{
 const feedback=question.querySelector('.feedback');
 function show(choice){const good=choice===Number(question.dataset.answer);feedback.hidden=false;feedback.className='feedback '+(good?'good':'bad');feedback.textContent=(good?'Correct 正確 · ':'Review 再想一想 · ')+question.dataset.explanation;question.querySelectorAll('.option').forEach(option=>{const n=Number(option.querySelector('input').value);option.classList.toggle('selected',n===choice);option.classList.toggle('correct-option',n===Number(question.dataset.answer))})}
 const previous=load().items?.[question.dataset.key]?.choice;
 if(Number.isInteger(previous)&&previous>=0&&previous<4){question.querySelector('input[value="'+previous+'"]').checked=true;show(previous)}
 question.querySelectorAll('input').forEach(input=>input.addEventListener('change',()=>{const choice=Number(input.value);show(choice);const data=load();data.items??={};const prior=data.items[question.dataset.key]||{};data.items[question.dataset.key]={...prior,choice,correct:choice===Number(question.dataset.answer),attempts:(prior.attempts||0)+1};save(data)}))
});
updateProgress();
