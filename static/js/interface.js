const CHAVE_DO_TEMA = 'potimaker-tema';

function temaSalvo() {
    try {
        return localStorage.getItem(CHAVE_DO_TEMA);
    } catch (erro) {
        return null;
    }
}

function aplicarTema(tema) {
    if (tema === 'escuro') {
        document.documentElement.setAttribute('data-tema', 'escuro');
    } else {
        document.documentElement.removeAttribute('data-tema');
    }
}

function alternarTema() {
    const escuroAgora = document.documentElement.getAttribute('data-tema') === 'escuro';
    const novoTema = escuroAgora ? 'claro' : 'escuro';
    try {
        localStorage.setItem(CHAVE_DO_TEMA, novoTema);
    } catch (erro) {
    }
    aplicarTema(novoTema);
}

const prefereEscuro = window.matchMedia('(prefers-color-scheme: dark)').matches;
aplicarTema(temaSalvo() || (prefereEscuro ? 'escuro' : 'claro'));

function prepararTema() {
    document.querySelectorAll('.botao-tema').forEach(function (botao) {
        botao.addEventListener('click', alternarTema);
    });
}

function prepararGaveta() {
    const gaveta = document.querySelector('.gaveta');
    const fundo = document.querySelector('.gaveta-fundo');
    const botaoAbrir = document.querySelector('.botao-perfil');
    const botaoFechar = document.querySelector('.gaveta-fechar');

    if (!gaveta || !fundo || !botaoAbrir || !botaoFechar) {
        return;
    }

    function abrir() {
        gaveta.classList.add('aberta');
        fundo.classList.add('visivel');
        botaoAbrir.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }

    function fechar() {
        gaveta.classList.remove('aberta');
        fundo.classList.remove('visivel');
        botaoAbrir.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    botaoAbrir.addEventListener('click', abrir);
    botaoFechar.addEventListener('click', fechar);
    fundo.addEventListener('click', fechar);
    document.addEventListener('keydown', function (evento) {
        if (evento.key === 'Escape') {
            fechar();
        }
    });
}

function prepararAbas() {
    const trilho = document.querySelector('.deslizante');
    const abas = document.querySelectorAll('.abas .aba');

    if (!trilho || abas.length === 0) {
        return;
    }

    abas.forEach(function (aba) {
        aba.addEventListener('click', function (evento) {
            const painel = document.querySelector(aba.getAttribute('href'));
            if (painel) {
                evento.preventDefault();
                painel.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }
        });
    });

    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
                abas.forEach(function (aba) {
                    aba.classList.toggle('ativa', aba.getAttribute('href') === '#' + entrada.target.id);
                });
            }
        });
    }, { root: trilho, threshold: 0.6 });

    Array.from(trilho.children).forEach(function (painel) {
        observador.observe(painel);
    });

    const inicial = trilho.querySelector('.painel-inicial');
    if (inicial) {
        const distancia = inicial.getBoundingClientRect().left - trilho.getBoundingClientRect().left;
        trilho.style.scrollBehavior = 'auto';
        trilho.scrollLeft = trilho.scrollLeft + distancia - 16;
        trilho.style.scrollBehavior = '';
    }
}

function prepararMensagens() {
    document.querySelectorAll('.mensagem').forEach(function (mensagem) {
        setTimeout(function () {
            mensagem.classList.add('sumindo');
        }, 6000);
        mensagem.addEventListener('animationend', function (evento) {
            if (evento.animationName === 'sumir') {
                mensagem.remove();
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    prepararTema();
    prepararGaveta();
    prepararAbas();
    prepararMensagens();
    document.documentElement.classList.add('tema-pronto');
});
