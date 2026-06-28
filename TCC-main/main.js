console.log("🚀 Inicializando...");

import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

// =========================
// CONFIGURAÇÕES
// =========================
const RAIO_TERRA = 5;
const TEXTURA_PATH = "/textures/earth.jpg";
const API_KEY = "AIzaSyCSP5XJE4ukwdTR1ca-QILJ5xZsThikzQc";

// ========== FUNÇÃO PARA DESENHAR ROTA ==========
function drawCurvePath(points3d) {
    const vectors = points3d.map(p => new THREE.Vector3(p[0], p[1], p[2]));
    const curve = new THREE.CatmullRomCurve3(vectors);
    const divisions = 500;
    const pointsOnCurve = curve.getPoints(divisions);
    const geometry = new THREE.BufferGeometry().setFromPoints(pointsOnCurve);
    const material = new THREE.LineBasicMaterial({ color: 0xffaa00 });
    const curveObject = new THREE.Line(geometry, material);

    if (window.currentRoute) {
        scene.remove(window.currentRoute);
    }
    window.currentRoute = curveObject;
    scene.add(curveObject);
}

// ========== CALCULAR ROTA E DESENHAR ==========
async function calculateAndDrawRoute(origem, destino) {
    try {
        const response = await fetch('http://localhost:5000/calcular_rota', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origem, destino })
        });
        const data = await response.json();
        if (data.erro) {
            alert(`❌ ${data.erro}`);
            return;
        }
        drawCurvePath(data.rota);
        alert(`🗺️ Rota de "${origem}" para "${destino}": ${data.distancia} km, ${data.duracao} minutos`);
    } catch (error) {
        console.error('Erro:', error);
        alert('❌ Erro ao calcular rota. Verifique se o servidor está rodando.');
    }
}



// =========================
// CENA 3D
// =========================
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 15);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.domElement.style.position = "fixed";
renderer.domElement.style.top = "0";
renderer.domElement.style.left = "0";
document.body.appendChild(renderer.domElement);


// =========================
// TERRA
// =========================
const geometry = new THREE.SphereGeometry(RAIO_TERRA, 64, 64);
const textureLoader = new THREE.TextureLoader();
const material = new THREE.MeshBasicMaterial({ map: textureLoader.load(TEXTURA_PATH) });
const earth = new THREE.Mesh(geometry, material);
scene.add(earth);

// =========================
// MARCADOR (para mostrar onde clicou)
// =========================
const markerGeometry = new THREE.SphereGeometry(0.2, 16, 16);
const markerMaterial = new THREE.MeshBasicMaterial({ color: 0xff3333 });
const marker = new THREE.Mesh(markerGeometry, markerMaterial);
marker.visible = false;
scene.add(marker);

// =========================
// CONTROLES
// =========================
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.05;

// =========================
// ANIMAÇÃO
// =========================
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();


const bgTexture = textureLoader.load(
    '/textures/fundo.jpg',
    () => {
        // Sucesso: define o fundo
        scene.background = bgTexture;
        console.log('✅ Fundo carregado com sucesso!');
    },
    undefined,
    (err) => {
        // Erro: fallback para cor
        console.warn('❌ Erro ao carregar fundo:', err);
        scene.background = new THREE.Color(0x0a0a2a); // azul escuro
    }
);
// Se a textura já estiver carregada no cache, define imediatamente
if (bgTexture.image) {
    scene.background = bgTexture;
}

// =========================
// STREET VIEW (IFRAME)
// =========================
function abrirStreetViewIframe(lat, lng) {
  console.log("Abrindo iframe Street View em:", lat, lng);

  const old = document.getElementById("street-view-iframe");
  if (old) old.remove();

  const container = document.createElement("div");
  container.id = "street-view-iframe";
  container.style.position = "fixed";
  container.style.top = "0";
  container.style.left = "0";
  container.style.width = "100vw";
  container.style.height = "100vh";
  container.style.zIndex = "9999";
  container.style.backgroundColor = "#000";

  const iframe = document.createElement("iframe");
  iframe.style.width = "100%";
  iframe.style.height = "100%";
  iframe.style.border = "none";
  iframe.src = `https://www.google.com/maps/embed/v1/streetview?key=${API_KEY}&location=${lat},${lng}&heading=0&pitch=0&fov=90`;

  const btn = document.createElement("button");
  btn.innerText = "FECHAR";
  btn.style.position = "absolute";
  btn.style.top = "20px";
  btn.style.right = "20px";
  btn.style.zIndex = "10000";
  btn.style.padding = "10px 20px";
  btn.style.background = "white";
  btn.style.border = "none";
  btn.style.cursor = "pointer";
  btn.onclick = () => container.remove();

  container.appendChild(iframe);
  container.appendChild(btn);
  document.body.appendChild(container);
}

// =========================
// ROTA (IFRAME)
// =========================
function abrirRotaIframe(origem, destino, modo = "carro") {
  const apiKey = "AIzaSyCSP5XJE4ukwdTR1ca-QILJ5xZsThikzQc";
  console.log(`🌍 Abrindo iframe de rota de ${origem} para ${destino}`);

     const modeMap = {
        "carro": "driving",
        "ônibus": "transit",
        "transporte público": "transit",
        "avião": "flying", 
        "a pé": "walking",
        "bicicleta": "bicycling"
    };
    const mode = modeMap[modo] || "driving";
    const url = `https://www.google.com/maps/embed/v1/directions?key=${API_KEY}&origin=${origem}&destination=${destino}&mode=${mode}`;;
    

  // Remove iframe antigo se existir
  const old = document.getElementById("rota-iframe");
  if (old) old.remove();

  // Cria o container e o iframe
  const container = document.createElement("div");
  container.id = "rota-iframe";
  container.style.position = "fixed";
  container.style.top = "0";
  container.style.left = "0";
  container.style.width = "100vw";
  container.style.height = "100vh";
  container.style.zIndex = "9999";
  container.style.backgroundColor = "#000";

  const iframe = document.createElement("iframe");
  iframe.style.width = "100%";
  iframe.style.height = "100%";
  iframe.style.border = "none";
  iframe.src = url;

  const btn = document.createElement("button");
  btn.innerText = "FECHAR";
  btn.style.position = "absolute";
  btn.style.top = "20px";
  btn.style.right = "20px";
  btn.style.zIndex = "10000";
  btn.style.padding = "10px 20px";
  btn.style.background = "white";
  btn.style.border = "none";
  btn.style.cursor = "pointer";
  btn.onclick = () => container.remove();

  container.appendChild(iframe);
  container.appendChild(btn);
  document.body.appendChild(container);
}

// =========================
// CONVERSÃO UV → LAT/LNG
// =========================
function uvParaLatLng(uv) {
  const lng = (uv.x - 0.5) * 360;
  const lat = (uv.y - 0.5) * 180;
  return { lat, lng };
}

// =========================
// VERIFICAR E ABRIR STREET VIEW (COM RAIO AMPLIADO)
// =========================
function verificarEAbrirStreetView(lat, lng) {
  if (!window.google || !google.maps) {
    alert("Google Maps ainda não carregou.");
    return;
  }

  const service = new google.maps.StreetViewService();
  service.getPanorama(
    { location: { lat, lng }, radius: 50000, source: google.maps.StreetViewSource.OUTDOOR },
    (data, status) => {
      if (status === "OK") {
        const pos = data.location.latLng;
        console.log("✅ Panorama encontrado em:", pos.lat(), pos.lng());
        abrirStreetViewIframe(pos.lat(), pos.lng());
      } else {
        alert("❌ Não há Street View num raio de 200m deste ponto.");
      }
    }
  );
}

// =========================
// DETECTOR DE DUPLO CLIQUE
// =========================
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

let clickTimer = null;
const DUPLO_CLIQUE_INTERVALO = 250;

window.addEventListener("click", (event) => {
  if (clickTimer) {
    clearTimeout(clickTimer);
    clickTimer = null;

    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(earth);

    if (intersects.length > 0) {
      const uv = intersects[0].uv;
      if (!uv) return;

      const pontoMundo = intersects[0].point;
      marker.position.copy(pontoMundo);
      marker.visible = true;

      const { lat, lng } = uvParaLatLng(uv);
      console.log(`🌍 Duplo clique: lat ${lat.toFixed(4)}, lng ${lng.toFixed(4)}`);

      verificarEAbrirStreetView(lat, lng);
    }

    return;
  }

  clickTimer = setTimeout(() => {
    clickTimer = null;
  }, DUPLO_CLIQUE_INTERVALO);
});

// =========================
// COMUNICAÇÃO COM O SERVIDOR FLASK
// =========================
function buscarComando() {
  fetch('http://localhost:5000/comando')
    .then(res => res.json())
    .then(cmd => {
      if (cmd.acao) {
        console.log('📡 Comando recebido:', cmd);
        executarComando(cmd.acao, cmd.dados);
      }
    })
    .catch(err => console.log('Aguardando servidor...'));
}

function executarComando(acao, dados) {
    if (acao === 'mostrar_local') {
        const lugar = dados.param;
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(lugar)}&limit=1`;
        fetch(url)
            .then(res => res.json())
            .then(data => {
                if (data && data[0]) {
                    const lat = parseFloat(data[0].lat);
                    const lng = parseFloat(data[0].lon);
                    console.log(`Coordenadas de ${lugar}: ${lat}, ${lng}`);
                    abrirStreetViewIframe(lat, lng);
                } else {
                    alert(`Não encontrei o local "${lugar}". Tente ser mais específico.`);
                }
            })
            .catch(err => console.error('Erro na geocodificação:', err));
    } else if (acao === 'rota') {
        const partes = dados.param.split('|');
        if (partes.length >= 2) {
            const origem = partes[0].trim();
            const destino = partes[1].trim();
            const modo = partes[2] ? partes[2].trim().toLowerCase() : "carro";
            abrirRotaIframe(origem, destino, modo);
        } else {
            console.error('Formato de rota inválido:', dados.param);
            alert('❌ Não consegui entender a origem e destino.');
        }
    } else if (acao === 'emocao') {
        const emocao = dados.emocao || 'NEUTRO';
        console.log(`😊 Emoção recebida: ${emocao}`);
        atualizarAvatar(emocao);
    }
}

function atualizarAvatar(emocao) {
    // Mapeamento emoção -> caminho da imagem
    const mapa = {
        'FELIZ': 'LUNA AS VARIAS FACEIS DE MIM/feliz.png',
        'TRISTE': 'LUNA AS VARIAS FACEIS DE MIM/triste.png',
        'PENSATIVA': 'LUNA AS VARIAS FACEIS DE MIM/pensativa.png',
        'BRAVA': 'LUNA AS VARIAS FACEIS DE MIM/brava.png',
        'NEUTRO': 'LUNA AS VARIAS FACEIS DE MIM/neutro.png'
    };
    
    const imgSrc = mapa[emocao] || mapa['NEUTRO'];
    const avatarEl = document.getElementById('avatar-luna');
    
    if (avatarEl) {
        // Pequena animação de fade (opcional)
        avatarEl.style.transition = 'opacity 0.3s';
        avatarEl.style.opacity = '0';
        setTimeout(() => {
            avatarEl.src = imgSrc;
            avatarEl.style.opacity = '1';
        }, 200);
    } else {
        console.warn('Elemento #avatar-luna não encontrado no HTML.');
    }
}



// Polling: consulta o servidor a cada 2 segundos
setInterval(buscarComando, 2000);