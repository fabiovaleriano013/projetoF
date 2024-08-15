function showSection(section) {
    var div = document.querySelector('main');
    var sections = div.querySelectorAll('section');
    sections.forEach(function (sectionElement) {
        if (sectionElement.id === section) {
            sectionElement.classList.remove('hide');
        } else {
            sectionElement.classList.add('hide');
        }
    });
    console.log("foi")
    icones = document.querySelectorAll('.icone');
    icone_id = 'icone_' + section;
    icones.forEach(function (iconeElement) {
        if (iconeElement.id === icone_id) {
            iconeElement.classList.add("fw-bold", "text-white"); // Adiciona as classes
        } else {
            iconeElement.classList.remove("fw-bold", "text-white"); // Remove as classes
        }
    });

}

var hoje = new Date();
var options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };

function salvarAnswer() {
    var form = $('#form_feedback')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/feedback/salvar_Answer/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('Feedback enviado com Sucesso!');
            // Limpar todos os campos do formulário
            $('#form_feedback input[type="text"]').val('');
            $('#form_feedback select').val('');
            $('#form_feedback textarea').val('');
            // Resetar o input de arquivo, se necessário
            $('#form_feedback input[type="file"]').val('');
            // Alerta de feedback enviado com sucesso
        },
        error: function (error) {
            console.error('Erro ao enviar feedback:', error);
        }
    });
}


function myFunction() {
    var x = document.getElementById("areaId").value;
    console.log(x)

    // Faça uma requisição AJAX para obter os comentários e exibi-los
    $.ajax({
        url: '/feedback/obter_feed/' + x + '/',
        type: 'GET',
        success: function (data) {
            // Limpe os comentários_container
            $('#feedback-list').empty();

            // Converta a string JSON de volta para um objeto JavaScript
            var mails = JSON.parse(data);

            // Mapeie os objetos para um novo array contendo apenas os campos desejados
            var mailsFiltrados = mails.map(function (mail) {
                return {
                    id: mail.pk,
                    area: mail.fields.area,
                    local: mail.fields.local,
                    datahora: mail.fields.datahora,
                    descricao: mail.fields.descricao,
                    status: mail.fields.status
                };
            });

            // Verifique se a lista de "mails" está vazia
            if (mailsFiltrados.length === 0) {
                // Crie a tag h1 com a mensagem
                var mensagem = document.createElement('h1');
                mensagem.textContent = 'Você ainda não recebeu nenhum feedback';

                // Adicione a mensagem à div de feedback-list
                var container = document.getElementById('feedback-list');
                container.appendChild(mensagem);
            } else {
                // Adicione os comentários filtrados à div
                mailsFiltrados.forEach(function (mail) {
                    var datahora = new Date(mail.datahora);

                    // Adiciona o comentário à div, limitando a 50 caracteres
                    // var comentarioTexto = comentario.comentario.length > 20 ? comentario.comentario.substring(0, 20) + '...' : comentario.comentario;
                    var divCard = document.createElement('div');
                    divCard.className = 'd-flex card2';
                    divCard.onclick = function () {
                        showDetails(mail.id);
                    };

                    ['p', 'h4', 'p', 'p'].forEach(function (tag, index) {
                        var element = document.createElement(tag);
                        element.className = (index === 0) ? 'status' : (index <= 2) ? 'textinho' : '';

                        if (index === 0) {
                            var cor;
                            var texto = mail.status;
                            if (texto == "Não Respondida") {
                                cor = 'blue';
                            } else if (texto == "Em Andamento") {
                                cor = 'yellow';
                            } else if (texto == "Não Resolvido") {
                                cor = 'red';
                            } else if (texto == "Resolvido") {
                                cor = 'green';
                            }
                            element.style.backgroundColor = cor;
                        } else if (index === 1) {
                            element.textContent = mail.area + " - " + mail.local;
                            var texto = element.textContent;
                            var limiteCaracteres = (window.innerWidth > 768) ? 40 : 18; // Verifica o tamanho da tela
                            var textoSemParenteses = texto.replace(/\(.*?\)/g, '').trim();
                            var textoFinal = textoSemParenteses;

                            // Limita os caracteres do texto final
                            element.textContent = limitarCaracteres(textoFinal, limiteCaracteres);

                        } else if (index === 2) {
                            var limiteCaracteres = (window.innerWidth > 768) ? 40 : 18; // Verifica o tamanho da tela
                            element.textContent = limitarCaracteres(mail.descricao, limiteCaracteres);
                        } else {
                            element.textContent = (datahora.toLocaleDateString() === hoje.toLocaleDateString()) ?
                                datahora.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) :
                                datahora.toLocaleDateString();
                        }
                        divCard.appendChild(element);
                    });

                    // Adicionar divCard ao seu contêiner HTML existente
                    var container = document.getElementById('feedback-list');  // Substitua 'seuContainerId' pelo ID do seu contêiner
                    container.appendChild(divCard);
                });
            }
        },
        error: function (error) {
            console.log("amor, ", error);
        }
    });
}

function limitarCaracteres(texto, limite) {
    return texto.length > limite ? texto.substring(0, limite) + '...' : texto;
}

function carregarComentarios(id, env_com) {
    $.ajax({
        url: '/feedback/obter_comentarios/' + id + '/',
        type: 'GET',
        success: function (data) {
            $('#comentarios_container').empty();
            var comentarios = JSON.parse(data);
            var comentariosFiltrados = comentarios.map(function (comentario) {
                return {
                    comentario: comentario.fields.comentario,
                    imagem: comentario.fields.imagem,
                    datahora: comentario.fields.datahora,
                    usuario: comentario.fields.usuario,
                };
            });

            var contador_coment = 0

            comentariosFiltrados.forEach(function (comentario) {
                if (comentario.comentario || comentario.imagem != '') {
                    var datahora = new Date(comentario.datahora);
                    var divComentario = $('<div>').addClass('coment');

                    divComentario.append('<p class="tipo_usuario">' + comentario.usuario + '</p>');

                    divComentario.append('<p class="datahora">' + datahora.toLocaleString() + '</p>');

                    if (comentario.comentario != '-' && comentario.comentario) {
                        divComentario.append('<p class="comentario_texto"></p>');
                    }
                    if (comentario.imagem != '') {
                        var match = comentario.imagem.match(/\/([^/]+)\.(\w+)$/);
                        divComentario.append('<img class="coment_imagem" src="{% static "coment/img" %}/' + match[0] + '">');
                        divComentario.addClass('coment_com_imagem');
                    }
                    $('#comentarios_container').append(divComentario);
                    a = document.getElementsByClassName('comentario_texto')[contador_coment];
                    $(a).text(comentario.comentario);
                    contador_coment = contador_coment + 1;
                }

                if (env_com == true) {
                    $('.informacoes').scrollTop($('.informacoes')[0].scrollHeight);
                } else {
                    $('.informacoes').scrollTop(0);
                }
            });

        },
        error: function (error) {
            console.log("Erro ao carregar comentários.");
        }
    });
}

function showDetails(id) {
    var modal = document.getElementById('Details');
    modal.style.display = 'flex';

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    document.getElementById('texto').value = '';

    // Faça uma requisição AJAX para obter os comentários e exibi-los
    $.ajax({
        url: '/feedback/modal_feedback/' + id + '/',
        type: 'GET',
        success: function (data) {

            // Converta a string JSON de volta para um objeto JavaScript
            var feedbacks = JSON.parse(data);

            // Mapeie os objetos para um novo array contendo apenas os campos desejados
            var feedbacksFiltrados = feedbacks.map(function (feed) {
                return {
                    descricao: feed.fields.descricao,
                    area: feed.fields.area,
                    local: feed.fields.local,
                    imagem: feed.fields.imagem,
                    status: feed.fields.status,
                    datahora: feed.fields.datahora,
                };
            });

            feedbacksFiltrados.forEach(function (feed) {
                var datahora = new Date(feed.datahora);
                $('#datahora2').text(datahora.toLocaleString());
                $('#descricao').text(feed.descricao);
                $('#area').text(feed.area);
                $('#local').text(feed.local);

                try{

                    select = document.getElementById('select_status');
                    var status = feed.status; // Obtenha o valor do status do template Django

                    for (var i = 0; i < select.options.length; i++) {
                        if (select.options[i].textContent === status) {
                            select.options[i].selected = true; // Seleciona a opção com o status correspondente
                            break;
                        }
                    }
                } catch (error) {
                    $('#status').text(feed.status);

                    var cor;
                    var status = feed.status;
                    if (status == "Não Respondida") {
                        cor = 'blue';
                    } else if (status == "Em Andamento") {
                        cor = 'yellow';
                    } else if (status == "Não Resolvido") {
                        cor = 'red';
                    } else if (status == "Resolvido") {
                        cor = 'green';
                    }
                    document.getElementById('status').style.color = cor;
                }

                var imagemElement = document.getElementById('imagem');

                if (feed.imagem != '') {
                    var match = feed.imagem.match(/\/([^/]+)\.(\w+)$/);
                    imagemElement.src = '{% static "img" %}' + match[0];
                    imagemElement.parentElement.style.textAlign = 'center';
                } else {
                    imagemElement.alt = 'Usuário não enviou foto';
                    imagemElement.src = '';
                }
            });
        },
        error: function (error) {
            console.log("abla maiusculo");
            console.log(error)
        }
    });
    document.getElementById('feedback_id').value = id;
    document.getElementById('feedback_id2').value = id;

    carregarComentarios(id, false);
}


function setarCorStatus() {
    var status = document.querySelectorAll('.status')
    status.forEach(function (element) {
        var cor;
        var texto = element.getAttribute('data-status')
        if (texto == "Não Respondida") {
            cor = 'blue';
        } else if (texto == "Em Andamento") {
            cor = 'yellow';
        } else if (texto == "Não Resolvido") {
            cor = 'red';
        } else if (texto == "Resolvido") {
            cor = 'green';
        }
        element.style.backgroundColor = cor;
        element.textContent = "";
    })
}


function newStatus() {
    var form = $('#form_status')[0];
    var formData = new FormData(form);
    var novoStatus = document.getElementById('select_status').value;
    var selectElement = document.getElementById('select_status');
    var selectedIndex = selectElement.selectedIndex;
    var novoStatus2 = selectElement.options[selectedIndex].textContent;
    var idFeedback = document.getElementById('feedback_id2').value;

    $.ajax({
        url: '/feedback/atualizar_status/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {

            id = document.getElementById('feedback_id').value;

            // Encontrar o elemento <p> correspondente pelo data-id
            var elemento = document.querySelector('p[data-id="' + id + '"]');
            elemento.setAttribute('data-status', novoStatus2);

            setarCorStatus();

            alert('Status atualizado com sucesso!');
            // Adicione aqui qualquer lógica adicional após o sucesso
        },
        error: function (error) {
            console.error('Erro ao atualizar o status:', error);
        }
    });
}

function salvarComentario() {
    var form = $('#form')[0];
    var formData = new FormData(form);
    texto = document.getElementById('texto').value;
    coment_img = document.getElementById('coment_img').value;

    if (!(texto == '' && coment_img == '')) {
        $.ajax({
            url: '/feedback/salvar_comentario/',  // Substitua pela sua URL de salvamento
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log('Comentário salvo com sucesso!');
                // Limpar os campos de texto e imagem
                document.getElementById('texto').value = '';
                document.getElementById('coment_img').value = '';


                // Adicione aqui qualquer lógica adicional após o sucesso
                var id = document.getElementById('feedback_id').value;
                carregarComentarios(id, true);
                // Adicione esta linha para rolar o scroll para o topo do modal

            },
            error: function (error) {
                console.error('Erro ao salvar o comentário:', error);
            }
        });
    } else {
        alert('Insira alguma informação em texto ou imagem');
    }

}

// Adicione um manipulador de eventos para o envio do formulário
$(document).ready(function () {
    $('#form').submit(function (event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        salvarComentario(); // Chama a função para enviar o formulário via AJAX
    });
});

function fecharModal(modal) {
    var modal = document.getElementById(modal);
    modal.style.display = 'none';
}


window.onload = function () {
    console.log('aca')
    if (window.innerWidth < 768) {
        console.log('lksjflksdj')
        document.getElementById('navbar_mobile').style.display = 'flex';
    } else {
        document.getElementById('navbar_pc').style.display = 'flex';
    }

    var textinho = document.querySelectorAll('.textinho')
    textinho.forEach(function (element) {
        var texto = element.textContent;
        var limiteCaracteres = (window.innerWidth > 768) ? 40 : 18; // Verifica o tamanho da tela
        var textoSemParenteses = texto.replace(/\(.*?\)/g, '').trim();
        var textoFinal = textoSemParenteses;

        // Limita os caracteres do texto final
        element.textContent = limitarCaracteres(textoFinal, limiteCaracteres);
    })

    setarCorStatus();
}



var contDiv = document.querySelector('.cont');

var arrayP = [];

// Essa função será chamada quando o formulário for enviado para atualizar os campos hidden.
function atualizarCamposHidden() {

    arrayP.length = 0;
    // Obtenha todos os campos do formulário
    var formElements = document.querySelectorAll('form .questao');

    // Itere pelos campos e adicione as informações aos arrays
    formElements.forEach(function (element) {
        arrayP.push(element.id)
    });
    document.getElementById("arrayP").value = JSON.stringify(arrayP);

    salvarAnswer();
}

function abrirCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            var video = document.createElement('video');
            video.srcObject = stream;
            video.autoplay = true;

            // Adicione o elemento de vídeo à sua página ou exiba em um modal
            document.body.appendChild(video);
        })
        .catch(function (error) {
            console.error('Erro ao acessar a câmera:', error);
            alert('Não foi possível acessar a câmera. Verifique se sua página está sendo carregada em um ambiente seguro (HTTPS) ou localhost.');
        });
}

function validarArquivo(input) {
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    const file = input.files[0];

    if (file && !allowedTypes.includes(file.type)) {
        alert('Por favor, selecione um arquivo de imagem válido.');
        input.value = ''; // Limpar o input para evitar envio acidental
    }
}