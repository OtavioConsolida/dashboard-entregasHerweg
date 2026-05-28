import re

with open('script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. resolveStatusLogico
old_resolve = '''function resolveStatusLogico(prazoStr, dataEntregaStr, situacaoOriginal) {
    const sitLower = situacaoOriginal ? String(situacaoOriginal).toLowerCase() : '';
    
    const prazoDt = parseDateBR(prazoStr);
    const entregaDt = parseDateBR(dataEntregaStr);
    
    const temPrazo = prazoDt && !isNaN(prazoDt);
    const temEntrega = entregaDt && !isNaN(entregaDt);

    if (temEntrega) {
        if (!temPrazo) {
            return 'Entregue sem prazo';
        } else {
            entregaDt.setHours(0,0,0,0);
            prazoDt.setHours(0,0,0,0);
            if (entregaDt > prazoDt) return 'Atrasado';
            else return 'No prazo';
        }
    } else {
        if (!temPrazo) {
            return 'Sem prazo';
        } else {
            const hoje = new Date();
            hoje.setHours(0,0,0,0);
            prazoDt.setHours(0,0,0,0);
            if (prazoDt < hoje) return 'Atrasado'; 
            else return 'Aguardando'; 
        }
    }
}'''

new_resolve = '''function resolveStatusLogico(prazoStr, dataEntregaStr, situacaoOriginal) {
    const prazoDt = parseDateBR(prazoStr);
    const entregaDt = parseDateBR(dataEntregaStr);
    
    const temPrazo = prazoDt && !isNaN(prazoDt);
    const temEntrega = entregaDt && !isNaN(entregaDt);

    if (!temPrazo) {
        return 'Sem prazo';
    }

    if (temEntrega) {
        entregaDt.setHours(0,0,0,0);
        prazoDt.setHours(0,0,0,0);
        if (entregaDt > prazoDt) return 'Entregue em atraso';
        else return 'No prazo';
    } else {
        const hoje = new Date();
        hoje.setHours(0,0,0,0);
        prazoDt.setHours(0,0,0,0);
        if (prazoDt < hoje) return 'Em atraso'; 
        else return 'No prazo'; 
    }
}'''

code = code.replace(old_resolve, new_resolve)

# 2. UI / HTML elements
code = code.replace("['No Prazo', 'Atrasado', 'Sem Prazo', 'Entregue sem Prazo']", "['No Prazo', 'Em Atraso', 'Sem Prazo', 'Entregue em Atraso']")
code = code.replace("data: [noPrazo, atrasado, semPrazo, entSemPrazo]", "data: [noPrazo, emAtraso, semPrazo, entregueAtraso]")
code = code.replace("let noPrazo = 0; let atrasado = 0; let semPrazo = 0; let entSemPrazo = 0;", "let noPrazo = 0; let emAtraso = 0; let entregueAtraso = 0; let semPrazo = 0;")
code = code.replace("else if (d.situacao === 'Atrasado') atrasado++;", "else if (d.situacao === 'Em atraso') emAtraso++;")
code = code.replace("else if (d.situacao === 'Entregue sem prazo') entSemPrazo++;", "else if (d.situacao === 'Entregue em atraso') entregueAtraso++;")

code = code.replace("if(d.situacao === 'Atrasado' || d.situacao === 'Sem prazo' || d.situacao === 'Entregue sem prazo')", "if(d.situacao === 'Em atraso' || d.situacao === 'Entregue em atraso' || d.situacao === 'Sem prazo')")
code = code.replace("stats[d.destino] = { atraso: 0, semPrazo: 0, entSemPrazo: 0 };", "stats[d.destino] = { emAtraso: 0, semPrazo: 0, entregueAtraso: 0 };")
code = code.replace("if(d.situacao === 'Atrasado') stats[d.destino].atraso++;", "if(d.situacao === 'Em atraso') stats[d.destino].emAtraso++;")
code = code.replace("if(d.situacao === 'Entregue sem prazo') stats[d.destino].entSemPrazo++;", "if(d.situacao === 'Entregue em atraso') stats[d.destino].entregueAtraso++;")

code = code.replace("label: 'Atrasado',", "label: 'Em Atraso',")
code = code.replace("label: 'Ent. Sem Prazo',", "label: 'Entregue em Atraso',")
code = code.replace("data: sorted.map(i => i[1].atraso)", "data: sorted.map(i => i[1].emAtraso)")
code = code.replace("data: sorted.map(i => i[1].entSemPrazo)", "data: sorted.map(i => i[1].entregueAtraso)")

code = code.replace("stats[d.transportadora] = { atrasos: 0, semPrazo: 0, entSemPrazo: 0, noPrazo: 0 };", "stats[d.transportadora] = { emAtraso: 0, semPrazo: 0, entregueAtraso: 0, noPrazo: 0 };")
code = code.replace("if (d.situacao === 'Atrasado') stats[d.transportadora].atrasos++;", "if (d.situacao === 'Em atraso') stats[d.transportadora].emAtraso++;")
code = code.replace("if (d.situacao === 'Entregue sem prazo') stats[d.transportadora].entSemPrazo++;", "if (d.situacao === 'Entregue em atraso') stats[d.transportadora].entregueAtraso++;")

code = code.replace("totalErros: v.atrasos + v.semPrazo + v.entSemPrazo", "totalErros: v.emAtraso + v.semPrazo + v.entregueAtraso")
code = code.replace("{ label: 'Atrasado', data: sorted.map(i => i[1].atrasos)", "{ label: 'Em Atraso', data: sorted.map(i => i[1].emAtraso)")
code = code.replace("{ label: 'Ent. Sem Prazo', data: sorted.map(i => i[1].entSemPrazo)", "{ label: 'Entregue em Atraso', data: sorted.map(i => i[1].entregueAtraso)")

code = code.replace("stats[t] = { atraso: 0, semPrazo: 0, entSemPrazo: 0, noPrazo: 0, score: 0 };", "stats[t] = { emAtraso: 0, semPrazo: 0, entregueAtraso: 0, noPrazo: 0, score: 0 };")
code = code.replace("if (d.situacao === 'Atrasado') stats[t].atraso++;", "if (d.situacao === 'Em atraso') stats[t].emAtraso++;")
code = code.replace("else if (d.situacao === 'Entregue sem prazo') stats[t].entSemPrazo++;", "else if (d.situacao === 'Entregue em atraso') stats[t].entregueAtraso++;")
code = code.replace("let total = s.atraso + s.semPrazo + s.entSemPrazo + s.noPrazo;", "let total = s.emAtraso + s.semPrazo + s.entregueAtraso + s.noPrazo;")
code = code.replace("<td><strong>${r.atraso}</strong></td>", "<td><strong>${r.emAtraso}</strong></td>")
code = code.replace("<td><strong>${r.entSemPrazo}</strong></td>", "<td><strong>${r.entregueAtraso}</strong></td>")
code = code.replace("<th>Atrasados</th>", "<th>Em Atraso</th>")
code = code.replace("<th>Entregue s/ Prazo</th>", "<th>Entregue em Atraso</th>")

# Data processing replacements
code = code.replace("d.situacao === 'No prazo' || d.situacao === 'Aguardando'", "d.situacao === 'No prazo'")
code = code.replace("d.situacao !== 'No prazo' && d.situacao !== 'Aguardando'", "d.situacao !== 'No prazo'")
code = code.replace("d.situacao === 'Sem prazo' || d.situacao === 'Entregue sem prazo'", "d.situacao === 'Sem prazo'")
code = code.replace("alert('Não há notas \"Sem prazo\" ou \"Entregue sem prazo\" neste filtro.')", "alert('Não há notas \"Sem prazo\" neste filtro.')")

# Checkboxes
code = code.replace(\"<input type='checkbox' id='chkAtrasados' class='mr-2' checked>\", \"<input type='checkbox' id='chkEmAtraso' class='mr-2' checked>\")
code = code.replace(\"<span>NFs em Atraso</span>\", \"<span>NFs Em Atraso</span>\")
code = code.replace(\"<input type='checkbox' id='chkEntregueSemPrazo' class='mr-2'>\", \"<input type='checkbox' id='chkEntregueEmAtraso' class='mr-2'>\")
code = code.replace(\"<span>Entregues sem Prazo</span>\", \"<span>Entregues em Atraso</span>\")

# Email modal
code = code.replace(\"const chkAtrasados = document.getElementById('chkAtrasados').checked;\", \"const chkEmAtraso = document.getElementById('chkEmAtraso').checked;\")
code = code.replace(\"const chkEntregueSemPrazo = document.getElementById('chkEntregueSemPrazo').checked;\", \"const chkEntregueEmAtraso = document.getElementById('chkEntregueEmAtraso').checked;\")
code = code.replace(\"if (chkAtrasados) allowedStatuses.push('Atrasado');\", \"if (chkEmAtraso) allowedStatuses.push('Em atraso');\")
code = code.replace(\"if (chkEntregueSemPrazo) allowedStatuses.push('Entregue sem prazo');\", \"if (chkEntregueEmAtraso) allowedStatuses.push('Entregue em atraso');\")
code = code.replace(\"const countAtrasados = notasEmail.filter(n => n.situacao === 'Atrasado').length;\", \"const countEmAtraso = notasEmail.filter(n => n.situacao === 'Em atraso').length;\")
code = code.replace(\"const countEntSemPrazo = notasEmail.filter(n => n.situacao === 'Entregue sem prazo').length;\", \"const countEntregueAtraso = notasEmail.filter(n => n.situacao === 'Entregue em atraso').length;\")
code = code.replace(\"if (countAtrasados > 0) {\", \"if (countEmAtraso > 0) {\")

# These were inside template literals, we must be careful
code = re.sub(r'Houve <strong>\$\{countAtrasados\} notas com atraso</strong>', 'Houve <strong>${countEmAtraso} notas em atraso</strong>', code)
code = re.sub(r'Houve <strong>\$\{countEntSemPrazo\} notas entregues sem prazo</strong>', 'Houve <strong>${countEntregueAtraso} notas entregues em atraso</strong>', code)
code = re.sub(r'Há <strong style="color: #991b1b;">\$\{countAtrasados\} NFs em atraso</strong>', 'Há <strong style="color: #991b1b;">${countEmAtraso} NFs em atraso</strong>', code)
code = re.sub(r'if \(n\.situacao === \'Atrasado\'\) \{', 'if (n.situacao === \\\'Em atraso\\\') {', code)
code = re.sub(r'\} else if \(n\.situacao === \'Entregue sem prazo\'\) \{', '} else if (n.situacao === \\\'Entregue em atraso\\\') {', code)

# Badges and UI updates
code = code.replace(\"if (r.status === 'Atrasado' || r.status === 'Em atraso' || r.status === 'Entregue em atraso')\", \"if (r.status === 'Em atraso' || r.status === 'Entregue em atraso')\")
code = code.replace(\"if (r.status === 'Aguardando') statusClass = 'bg-yellow-100 text-yellow-800';\", \"\")
code = code.replace(\"<td><span class=\\\"status-badge ${statusClass}\\\">Aguardando</span></td>\", \"<td><span class=\\\"status-badge ${statusClass}\\\">${r.situacao || r.status || 'No prazo'}</span></td>\")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('Replacement complete.')
