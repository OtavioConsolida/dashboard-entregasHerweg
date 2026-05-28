import re

with open('script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. resolveStatusLogico
old_resolve = '''function resolveStatusLogico(prazoStr, dataEntregaStr, situacaoOriginal) {
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

new_resolve = '''function resolveStatusLogico(prazoStr, dataEntregaStr, situacaoOriginal) {
    const prazoDt = parseDateBR(prazoStr);
    const entregaDt = parseDateBR(dataEntregaStr);
    
    const temPrazo = prazoDt && !isNaN(prazoDt);
    const temEntrega = entregaDt && !isNaN(entregaDt);

    if (temEntrega) {
        if (!temPrazo) return 'Entregue sem prazo';
        entregaDt.setHours(0,0,0,0);
        prazoDt.setHours(0,0,0,0);
        if (entregaDt > prazoDt) return 'Entregue em atraso';
        else return 'No prazo';
    } else {
        if (!temPrazo) return 'Sem prazo';
        const hoje = new Date();
        hoje.setHours(0,0,0,0);
        prazoDt.setHours(0,0,0,0);
        if (prazoDt < hoje) return 'Em atraso'; 
        else return 'No prazo'; 
    }
}'''
code = code.replace(old_resolve, new_resolve)

# 2. SLA Chart
code = code.replace("let noPrazo = 0; let emAtraso = 0; let entregueAtraso = 0; let semPrazo = 0;", "let noPrazo = 0; let emAtraso = 0; let entregueAtraso = 0; let semPrazo = 0; let entSemPrazo = 0;")
code = code.replace("else if (d.situacao === 'Sem prazo') semPrazo++;", "else if (d.situacao === 'Sem prazo') semPrazo++;\n        else if (d.situacao === 'Entregue sem prazo') entSemPrazo++;")
code = code.replace("labels: ['No Prazo', 'Em Atraso', 'Sem Prazo', 'Entregue em Atraso']", "labels: ['No Prazo', 'Em Atraso', 'Entregue em Atraso', 'Sem Prazo', 'Entregue s/ Prazo']")
code = code.replace("data: [noPrazo, emAtraso, semPrazo, entregueAtraso]", "data: [noPrazo, emAtraso, entregueAtraso, semPrazo, entSemPrazo]")
code = code.replace("backgroundColor: [colors.success, colors.danger, colors.warning, colors.info]", "backgroundColor: [colors.success, colors.danger, '#f97316', colors.warning, colors.info]")

# 3. Regions Chart
code = code.replace("if(d.situacao === 'Em atraso' || d.situacao === 'Entregue em atraso' || d.situacao === 'Sem prazo')", "if(d.situacao === 'Em atraso' || d.situacao === 'Entregue em atraso' || d.situacao === 'Sem prazo' || d.situacao === 'Entregue sem prazo')")
code = code.replace("stats[d.destino] = { emAtraso: 0, semPrazo: 0, entregueAtraso: 0 };", "stats[d.destino] = { emAtraso: 0, entregueAtraso: 0, semPrazo: 0, entSemPrazo: 0 };")
code = code.replace("if(d.situacao === 'Sem prazo') stats[d.destino].semPrazo++;", "if(d.situacao === 'Sem prazo') stats[d.destino].semPrazo++;\n            if(d.situacao === 'Entregue sem prazo') stats[d.destino].entSemPrazo++;")
code = code.replace("label: 'Entregue em Atraso',\n                    data: sorted.map(i => i[1].entregueAtraso),\n                    backgroundColor: colors.info", "label: 'Entregue em Atraso',\n                    data: sorted.map(i => i[1].entregueAtraso),\n                    backgroundColor: '#f97316'\n                },\n                {\n                    label: 'Entregue s/ Prazo',\n                    data: sorted.map(i => i[1].entSemPrazo),\n                    backgroundColor: colors.info")

# 4. Bottlenecks Chart
code = code.replace("stats[d.transportadora] = { emAtraso: 0, semPrazo: 0, entregueAtraso: 0, noPrazo: 0 };", "stats[d.transportadora] = { emAtraso: 0, entregueAtraso: 0, semPrazo: 0, entSemPrazo: 0, noPrazo: 0 };")
code = code.replace("if (d.situacao === 'Sem prazo') stats[d.transportadora].semPrazo++;", "if (d.situacao === 'Sem prazo') stats[d.transportadora].semPrazo++;\n        if (d.situacao === 'Entregue sem prazo') stats[d.transportadora].entSemPrazo++;")
code = code.replace("totalErros: v.emAtraso + v.semPrazo + v.entregueAtraso", "totalErros: v.emAtraso + v.entregueAtraso + v.semPrazo + v.entSemPrazo")
code = code.replace("{ label: 'Entregue em Atraso', data: sorted.map(i => i[1].entregueAtraso), backgroundColor: colors.info }", "{ label: 'Entregue em Atraso', data: sorted.map(i => i[1].entregueAtraso), backgroundColor: '#f97316' },\n                { label: 'Ent. Sem Prazo', data: sorted.map(i => i[1].entSemPrazo), backgroundColor: colors.info }")

# 5. Ranking
code = code.replace("stats[t] = { emAtraso: 0, semPrazo: 0, entregueAtraso: 0, noPrazo: 0, score: 0 };", "stats[t] = { emAtraso: 0, entregueAtraso: 0, semPrazo: 0, entSemPrazo: 0, noPrazo: 0, score: 0 };")
code = code.replace("else if (d.situacao === 'Sem prazo') stats[t].semPrazo++;", "else if (d.situacao === 'Sem prazo') stats[t].semPrazo++;\n        else if (d.situacao === 'Entregue sem prazo') stats[t].entSemPrazo++;")
code = code.replace("let total = s.emAtraso + s.semPrazo + s.entregueAtraso + s.noPrazo;", "let total = s.emAtraso + s.entregueAtraso + s.semPrazo + s.entSemPrazo + s.noPrazo;")
code = code.replace("<td><strong>${r.entregueAtraso}</strong></td>", "<td><strong>${r.entregueAtraso}</strong></td>\n            <td><strong>${r.entSemPrazo}</strong></td>")
code = code.replace("<th>Entregue em Atraso</th>", "<th>Entregue em Atraso</th>\n                                        <th>Entregue s/ Prazo</th>")

# 6. Admin Export
code = code.replace("d.situacao === 'Sem prazo'", "d.situacao === 'Sem prazo' || d.situacao === 'Entregue sem prazo'")
code = code.replace("alert('Não há notas \"Sem prazo\" neste filtro.')", "alert('Não há notas \"Sem prazo\" ou \"Entregue sem prazo\" neste filtro.')")

# 7. Checkboxes HTML
old_chk = '''<label class="flex items-center text-sm cursor-pointer">
                                        <input type='checkbox' id='chkEntregueEmAtraso' class='mr-2'>
                                        <span>Entregues em Atraso</span>
                                    </label>'''
new_chk = '''<label class="flex items-center text-sm cursor-pointer">
                                        <input type='checkbox' id='chkEntregueEmAtraso' class='mr-2'>
                                        <span>Entregues em Atraso</span>
                                    </label>
                                    <label class="flex items-center text-sm cursor-pointer">
                                        <input type='checkbox' id='chkEntregueSemPrazo' class='mr-2'>
                                        <span>Entregues s/ Prazo</span>
                                    </label>'''
code = code.replace(old_chk, new_chk)

# 8. Email logic
code = code.replace("const chkEntregueEmAtraso = document.getElementById('chkEntregueEmAtraso').checked;", "const chkEntregueEmAtraso = document.getElementById('chkEntregueEmAtraso').checked;\n        const chkEntregueSemPrazo = document.getElementById('chkEntregueSemPrazo').checked;")
code = code.replace("if (chkEntregueEmAtraso) allowedStatuses.push('Entregue em atraso');", "if (chkEntregueEmAtraso) allowedStatuses.push('Entregue em atraso');\n        if (chkEntregueSemPrazo) allowedStatuses.push('Entregue sem prazo');")
code = code.replace("const countEntregueAtraso = notasEmail.filter(n => n.situacao === 'Entregue em atraso').length;", "const countEntregueAtraso = notasEmail.filter(n => n.situacao === 'Entregue em atraso').length;\n        const countEntSemPrazo = notasEmail.filter(n => n.situacao === 'Entregue sem prazo').length;")

old_html_gen = '''if (countEntregueAtraso > 0) {
            html += `<p style="margin: 5px 0; font-size: 14px; color: #4a5568;">
                        <i class="fas fa-exclamation-circle" style="color: #ed8936;"></i> 
                        Houve <strong>${countEntregueAtraso} notas entregues em atraso</strong> fora do prazo estipulado.
                     </p>`;
        }'''
new_html_gen = '''if (countEntregueAtraso > 0) {
            html += `<p style="margin: 5px 0; font-size: 14px; color: #4a5568;">
                        <i class="fas fa-exclamation-circle" style="color: #ed8936;"></i> 
                        Houve <strong>${countEntregueAtraso} notas entregues em atraso</strong> fora do prazo estipulado.
                     </p>`;
        }
        if (countEntSemPrazo > 0) {
            html += `<p style="margin: 5px 0; font-size: 14px; color: #4a5568;">
                        <i class="fas fa-exclamation-circle" style="color: #4299e1;"></i> 
                        Houve <strong>${countEntSemPrazo} notas entregues sem prazo</strong> previamente estipulado.
                     </p>`;
        }'''
code = code.replace(old_html_gen, new_html_gen)

old_loop = '''} else if (n.situacao === 'Entregue em atraso') {
                statusStyle = 'background-color: #ed8936; color: #ffffff;';
            } else if (n.situacao === 'Sem prazo') {'''
new_loop = '''} else if (n.situacao === 'Entregue em atraso') {
                statusStyle = 'background-color: #f97316; color: #ffffff;';
            } else if (n.situacao === 'Entregue sem prazo') {
                statusStyle = 'background-color: #4299e1; color: #ffffff;';
            } else if (n.situacao === 'Sem prazo') {'''
code = code.replace(old_loop, new_loop)

# 9. Status Badges CSS
code = code.replace("if (r.status === 'Em atraso' || r.status === 'Entregue em atraso')", "if (r.status === 'Em atraso' || r.status === 'Entregue em atraso') statusClass = 'bg-red-100 text-red-800';\n        if (r.status === 'Entregue sem prazo')")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('Success')
