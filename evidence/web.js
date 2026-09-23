const $ = id => document.getElementById(id);
let selected = null;
async function api(path, options = {}) {
  const response = await fetch('/api' + path, {...options, headers: {'Content-Type': 'application/json'}});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'No se pudo completar la operación');
  return data;
}
function node(tag, value, className) {
  const element = document.createElement(tag);
  element.textContent = value;
  if (className) element.className = className;
  return element;
}
function message(id, text, error = false) { $(id).textContent = text; $(id).className = error ? 'error' : ''; }
async function load() {
  try {
    await api('/health');
    const alerts = await api('/alertas?severidad=' + encodeURIComponent($('filter').value));
    message('connection', 'API conectada · Datos guardados en PostgreSQL · Vista actualizada');
    $('total').textContent = alerts.length;
    $('urgent').textContent = alerts.filter(a => ['alta','critica'].includes(a.severidad)).length;
    $('escalated').textContent = alerts.filter(a => a.estado === 'escalada').length;
    $('alerts').replaceChildren();
    if (!alerts.length) $('alerts').append(node('p', 'No hay alertas para mostrar. Registra una o cambia el filtro.', 'muted'));
    for (const a of alerts) {
      const row = node('button', '', 'alert-row' + (a.id === selected ? ' selected' : ''));
      row.type = 'button'; row.append(node('strong', `#${a.id} · ${a.titulo}`));
      const meta = node('span', '', 'meta');
      meta.append(node('span', a.hostname), node('span', a.severidad, 'pill ' + a.severidad), node('span', a.estado));
      row.append(meta); row.addEventListener('click', () => detail(a.id)); $('alerts').append(row);
    }
  } catch (e) { message('connection', 'No hay conexión: ' + e.message, true); $('alerts').replaceChildren(node('p', 'No se pudieron cargar las alertas.', 'error')); }
}
async function detail(id) {
  try {
    const a = await api('/alertas/' + id); selected = id;
    $('empty-detail').hidden = true; $('detail').hidden = false;
    $('detail-content').replaceChildren(node('h3', `#${a.id} · ${a.titulo}`), node('p', `${a.hostname} · Severidad: ${a.severidad} · Estado: ${a.estado}`), node('p', a.descripcion || 'Sin descripción', 'muted'));
    $('new-severity').value = a.severidad;
    $('history').replaceChildren();
    for (const h of a.acciones) $('history').append(node('li', `${h.creado_en} · ${h.tipo} · ${h.nota || 'Sin nota'} · Actor: ${h.actor}`));
    await load();
  } catch (e) { message('action-message', e.message, true); }
}
$('new-alert').addEventListener('submit', async event => {
  event.preventDefault(); const button = event.submitter; button.disabled = true;
  try {
    const data = Object.fromEntries(new FormData(event.target));
    const a = await api('/alertas', {method: 'POST', body: JSON.stringify(data)});
    message('form-message', `Alerta #${a.id} guardada en PostgreSQL.`); event.target.reset(); await detail(a.id);
  } catch(e) { message('form-message', e.message, true); } finally { button.disabled = false; }
});
$('example').addEventListener('click', () => { $('title').value = 'Ejecución sospechosa simulada'; $('host').value = 'EQUIPO-LAB-01'; $('severity').value = 'alta'; $('description').value = 'Alerta ficticia para practicar clasificación y trazabilidad. No corresponde a un incidente real.'; });
$('action').addEventListener('change', () => { $('new-severity-group').hidden = $('action').value !== 'clasificar'; });
$('action-form').addEventListener('submit', async event => {
  event.preventDefault(); if (selected === null) return;
  const button = event.submitter; button.disabled = true;
  try {
    await api(`/alertas/${selected}/acciones`, {method: 'POST', body: JSON.stringify({tipo: $('action').value, nota: $('note').value, severidad: $('new-severity').value})});
    message('action-message', 'Acción guardada. El escalamiento es solo una simulación.'); $('note').value = ''; await detail(selected);
  } catch(e) { message('action-message', e.message, true); } finally { button.disabled = false; }
});
$('refresh').addEventListener('click', load); $('filter').addEventListener('change', load); load();
