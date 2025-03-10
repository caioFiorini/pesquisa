// Captura elementos do HTML
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const buttonSetAG = document.getElementById('button_set_AG');

// Inputs dinâmicos 
const algoritmoSelect = document.getElementById("algoritmo-select");
const parametrosContainer = document.getElementById("parametros-container");
const setParamsBtn = document.getElementById("set-params-btn");

// Captura todos os inputs dentro da classe `.input_group`
const inputGroups = document.querySelectorAll(".input_group");

// Captura os checkboxes da otimização
const checkboxClassica = document.getElementById('opcao1');
const checkboxOtimizada = document.getElementById('opcao2');

// Função para capturar os valores dos inputs
function getInputValues() {
    let inputValues = {};
    
    inputGroups.forEach(input => {
        inputValues[input.placeholder] = input.value || input.placeholder; // Usa o valor ou o placeholder
    });

    return inputValues;
}

// Função para capturar o estado dos checkboxes
function getCheckboxValues() {
    return {
        classica: checkboxClassica.checked,
        otimizada: checkboxOtimizada.checked
    };
}

// Evento para o botão "Set" do Algoritmo Genético
buttonSetAG.addEventListener("click", () => {
    const inputs = getInputValues();
    const checkboxes = getCheckboxValues();

    console.log("Dados Capturados:");
    console.log("Inputs:", inputs);
    console.log("Checkboxes:", checkboxes);

    // Simulação de envio para o Flask (aqui entrará a requisição HTTP futuramente)
    enviarDadosParaFlask(inputs, checkboxes);
});

// Simulação de função para enviar ao Flask
function enviarDadosParaFlask(inputs, checkboxes) {
    console.log("Enviando para Flask...");
    // Aqui entrará a chamada AJAX ou fetch() para o backend Flask
}

// ---------------- DRAG & DROP ----------------

// Prevenir comportamentos padrão
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => e.preventDefault());
});

// Adicionar efeito visual ao arrastar
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.classList.add('highlight');
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.classList.remove('highlight');
});

// Lidar com o drop
dropArea.addEventListener('drop', (e) => {
    let file = e.dataTransfer.files[0];
    validarCSV(file);
});

// Clique para selecionar arquivo
dropArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    let file = e.target.files[0];
    validarCSV(file);
});

// Valida se o arquivo é CSV
function validarCSV(file) {
    if (!file) return;

    if (file.type === 'text/csv' || file.name.endsWith('.csv')) {
        fileInfo.textContent = 'Arquivo válido: ' + file.name;
        fileInfo.style.color = 'green';
    
        lerCsv(file);
    } else {
        fileInfo.textContent = 'Erro: Apenas arquivos CSV são permitidos';
        fileInfo.style.color = 'red';
    }
}

// Lê o CSV (simplesmente exibe no console por enquanto)
function lerCsv(file) {
    const reader = new FileReader();
    reader.onload = function(event) {
        console.log("Conteúdo do CSV:", event.target.result);
    };
    reader.readAsText(file);
}


// Imputs dinâmicos


// Lista de parâmetros por algoritmo
const parametrosPorAlgoritmo = {
    decision_tree: [
        { label: "Max Depth: ", name: "max_depth", type: "number", placeholder: "5" },
        { label: "Min Samples Split: ", name: "min_samples_split", type: "number", placeholder: "2" },
        { label: "Min Samples Leaf: ", name: "min_samples_leaf", type: "number", placeholder: "1" },

        { label: "Max Features: ", name: "max_features", type: "select", options: ["auto", "sqrt", "log2", "None"] },
        { label: "Splitter: ", name: "splitter", type: "select", options: ["best", "random"] },
        { label: "Criterion: ", name: "criterion", type: "select", options: ["gini", "entropy"] },

        { label: "Min Impurity Decrease: ", name: "min_impurity_decrease", type: "number", placeholder: "0.0" },
        { label: "Random State: ", name: "random_state", type: "number", placeholder: "None" },
        { label: "Class Weight: ", name: "class_weight", type: "select", options: ["None", "balanced"] },
        { label: "CCP Alpha: ", name: "ccp_alpha", type: "number", placeholder: "0.0" },
        { label: "Min Weight Fraction Leaf: ", name: "min_weight_fraction_leaf", type: "number", placeholder: "0.0" }
    ],
    knn: [
        { label: "Nº de Vizinhos", name: "n_neighbors", type: "number", placeholder: "5" },
        { label: "Peso", name: "weights", type: "select", options: ["uniform", "distance"] },
        { label: "Algoritmo", name: "algorithm", type: "select", options: ["auto", "ball_tree", "kd_tree", "brute"] },
        { label: "Leaf Size", name: "leaf_size", type: "number", placeholder: "30" },
        { label: "P (Distância Minkowski)", name: "p", type: "number", placeholder: "2" },
        { label: "Metric", name: "metric", type: "select", options: ["minkowski", "euclidean", "manhattan", "chebyshev"] },
        { label: "Metric Params", name: "metric_params", type: "text", placeholder: "None" },
        { label: "N_jobs", name: "n_jobs", type: "number", placeholder: "None" }
    ]
};

// Função que gera os inputs dinamicamente
function gerarInputs(algoritmo) {
    parametrosContainer.innerHTML = "";

    parametrosPorAlgoritmo[algoritmo].forEach(param => {
        const div = document.createElement("div");
        div.classList.add("input-group");

        const label = document.createElement("label");
        label.textContent = param.label;

        let inputElement;

        if (param.type === "select" && param.options) { // Garante que options existe
            inputElement = document.createElement("select");
            inputElement.name = param.name;

            param.options.forEach(optionValue => {
                const option = document.createElement("option");
                option.value = optionValue;
                option.textContent = optionValue;
                inputElement.appendChild(option);
            });
        } else {
            inputElement = document.createElement("input");
            inputElement.type = param.type || "text";
            inputElement.name = param.name;
            inputElement.placeholder = param.placeholder || "";
        }

        div.appendChild(label);
        div.appendChild(inputElement);
        parametrosContainer.appendChild(div);
    });
}

// Quando o usuário escolhe um algoritmo, gera os inputs automaticamente
algoritmoSelect.addEventListener("change", (event) => {
    gerarInputs(event.target.value);
});

// Captura os valores ao clicar no botão "Set"
setParamsBtn.addEventListener("click", () => {
    const inputs = document.querySelectorAll("#parametros-container input, #parametros-container select");
    let valores = {};

    inputs.forEach(input => {
        valores[input.name] = input.value;
    });

    console.log("Valores capturados:", valores);
});

// Evento para capturar os valores ao clicar no botão "Set"
setParamsBtn.addEventListener("click", capturarValores);