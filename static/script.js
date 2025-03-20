// Carrega os imóveis com base nos parâmetros da URL ao abrir a página
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const params = urlParams.toString();
    fetch(params ? `/imoveis/busca?${params}` : '/imoveis')
        .then(response => {
            if (!response.ok) throw new Error('Erro na resposta do servidor');
            return response.json();
        })
        .then(imoveis => exibirImoveis(imoveis))
        .catch(error => console.error('Erro:', error));
};

// Redireciona o filtro para a mesma página com parâmetros
document.getElementById('busca-form').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log('Botão Filtrar clicado!');
    const formData = new FormData(this);
    const params = new URLSearchParams(formData).toString();
    window.location.href = `/static/index.html?${params}`;
});

// Limpa a busca e recarrega todos os imóveis
document.getElementById('limpar-busca').addEventListener('click', function() {
    window.location.href = '/static/index.html'; // Recarrega sem parâmetros
});

function exibirImoveis(imoveis) {
    const resultados = document.getElementById('resultados');
    const urlParams = new URLSearchParams(window.location.search);
    const objetivo = urlParams.get('objetivo') || 'alugar';
    resultados.innerHTML = '<h2>Todos os Imóveis</h2>';
    imoveis.forEach(imovel => {
        const preco = objetivo === 'comprar' ? imovel.preco_venda : imovel.preco_aluguel;
        const precoLabel = objetivo === 'comprar' ? 'R$' + preco.toFixed(2) : 'R$' + preco.toFixed(2) + '/mês';
        resultados.innerHTML += `
            <div class="card" onclick="window.open('/static/detalhes.html?id=${imovel.id}', '_blank')">
                <img src="${imovel.foto_url}" alt="${imovel.localizacao}" class="imovel-foto">
                <div class="card-info">
                    <p><strong>${imovel.localizacao}</strong> - ${imovel.tipo} (${imovel.quartos} quartos)</p>
                    <p>${precoLabel}</p>
                </div>
            </div>`;
    });
}

function abrirAgendamento(id, localizacao) {
    document.getElementById('imovel-id').value = id;
    document.getElementById('imovel-nome').textContent = localizacao;
    document.getElementById('modal-agendamento').style.display = 'block';
}

function fecharModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.getElementById('agendamento-msg').textContent = '';
}

document.getElementById('agendamento-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = {
        imovel_id: formData.get('imovel_id'),
        data_visita: formData.get('data_visita'),
        horario: formData.get('horario')
    };

    fetch('/agendar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('agendamento-msg').textContent = result.message;
    })
    .catch(error => console.error('Erro:', error));
});

function toggleChat() {
    const chatBody = document.getElementById('chatbot-body');
    chatBody.style.display = chatBody.style.display === 'block' ? 'none' : 'block';
}

function enviarMensagem() {
    const input = document.getElementById('chat-input');
    const mensagem = input.value;
    const messages = document.getElementById('chat-messages');
    messages.innerHTML += `<p><strong>Você:</strong> ${mensagem}</p>`;
    input.value = '';

    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pergunta: mensagem })
    })
    .then(response => response.json())
    .then(data => {
        messages.innerHTML += `<p><strong>Bot:</strong> ${data.resposta}</p>`;
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(error => console.error('Erro:', error));
}