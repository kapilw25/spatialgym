const byId=Object.fromEntries(TREE.map(n=>[n.id,n]));
const buttons=[...document.querySelectorAll('nav.tabs button')];
const bars=[...document.querySelectorAll('nav.tabs[data-parent]')];
const panels=[...document.querySelectorAll('.panel')];
const leaves=TREE.filter(n=>n.leaf).map(n=>n.id);
function chain(id){const out=[];let n=byId[id];while(n){out.unshift(n.id);n=n.parent?byId[n.parent]:null;}return out;}
function activate(leafId,push){
  if(!byId[leafId]||!byId[leafId].leaf) leafId=leaves[0];
  const path=chain(leafId);
  buttons.forEach(b=>b.setAttribute('aria-selected',path.includes(b.dataset.node)));
  bars.forEach(b=>b.classList.toggle('active',path.includes(b.dataset.parent)));
  panels.forEach(p=>p.classList.toggle('active',p.id==='tab-'+leafId));
  if(push)history.replaceState(null,'','#tab-'+leafId);
}
buttons.forEach(b=>b.addEventListener('click',()=>activate(b.dataset.leaf,true)));
document.addEventListener('keydown',e=>{if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;if(e.target.closest('input,textarea'))return;
  const cur=(location.hash.startsWith('#tab-')?location.hash.slice(5):leaves[0]);const i=Math.max(0,leaves.indexOf(cur));
  activate(leaves[(i+(e.key==='ArrowRight'?1:leaves.length-1))%leaves.length],true);});
document.querySelectorAll('.panel table').forEach(t=>{const w=document.createElement('div');w.className='tablewrap';t.parentNode.insertBefore(w,t);w.appendChild(t);});
document.querySelectorAll('.panel a[href^="http"]').forEach(a=>{a.target='_blank';a.rel='noopener';});
document.querySelectorAll('a[href^="#tab-"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();activate(a.getAttribute('href').slice(5),true);window.scrollTo(0,0);}));
window.addEventListener('hashchange',()=>activate(location.hash.replace('#tab-',''),false));
activate(location.hash.startsWith('#tab-')?location.hash.slice(5):leaves[0],false);

// ---- decisions log drawer: the badge always shows the total number of entries (no browser storage)
(function(){
  const bell=document.getElementById('bell'); if(!bell) return;
  const drawer=document.getElementById('drawer'), badge=document.getElementById('badge'), count=document.getElementById('dcount'), items=[...drawer.querySelectorAll('li')];
  badge.textContent=items.length>99?'99+':String(items.length); badge.hidden=items.length===0; count.textContent=items.length+' entries, newest first';
  function toggle(open){drawer.hidden=!open;bell.setAttribute('aria-expanded',String(open));}
  bell.addEventListener('click',e=>{e.stopPropagation();toggle(drawer.hidden);});
  drawer.addEventListener('click',e=>e.stopPropagation());
  document.addEventListener('click',()=>toggle(false));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')toggle(false);});
})();
