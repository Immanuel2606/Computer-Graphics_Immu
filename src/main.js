/* =================================================================
   main.js — Real-Time 3D City Navigation & Visibility Analysis
   Projection + Hidden Surface Removal (HSR) using Three.js
   ================================================================= */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// =================================================================
// 1. GLOBAL STATE & REFERENCES
// =================================================================

let scene, renderer;
let perspectiveCamera, orthographicCamera, activeCamera;
let isPerspective = true;
let isFirstPersonNav = false; // true when player is walking in first-person

// City model and bounds
let cityModel = null;
const cityBoundingBox = new THREE.Box3();
const cityCenter = new THREE.Vector3();
const citySize = new THREE.Vector3();
const obstacleMeshes = []; // solid building meshes used for collision detection

// First-person navigation configuration
const EYE_HEIGHT = 1.8;           // standard human eye height in meters
const WALK_SPEED = 12.0;          // base walking speed (units/second)
const SPRINT_MULTIPLIER = 1.8;    // sprint multiplier (Shift key)
const LOOK_SENSITIVITY = 0.0022;  // mouse look sensitivity
const PLAYER_RADIUS = 0.85;       // horizontal collision bumper radius

let yaw = 0;    // horizontal rotation (radians)
let pitch = 0;  // vertical rotation (radians)
const keysPressed = {};

// Saved overview camera state
const overviewCameraPosition = new THREE.Vector3(420, 360, 460);
const overviewCameraTarget = new THREE.Vector3(0, 50, 0);

// Verified open street intersection start position
const streetStartPosition = new THREE.Vector3(-60.5, EYE_HEIGHT, 145.5);
let streetStartFacingYaw = Math.PI * 0.75; // facing North-East toward core towers

// Visibility Analysis (Line-of-Sight)
let visibilityModeActive = true;
let visRayLine = null;
let visTargetMarker = null;

// Performance & Animation
const clock = new THREE.Clock();
let frameCount = 0;
let lastFpsTime = performance.now();

// Cached DOM Elements
let dom = {};

// =================================================================
// 2. INITIALIZATION
// =================================================================

function init() {
  cacheDOMElements();

  // Create Scene
  scene = new THREE.Scene();
  // Modern crisp daylight Manhattan sky
  scene.background = new THREE.Color(0xbddff7);
  // Gentle atmospheric fog (replaces dark fog)
  scene.fog = new THREE.FogExp2(0xbddff7, 0.0006);

  // Create WebGL Renderer with Depth Buffer for Hidden Surface Removal
  renderer = new THREE.WebGLRenderer({
    canvas: dom.canvas,
    antialias: true,
    powerPreference: 'high-performance',
    depth: true, // Hardware 24-bit Z-buffer for HSR
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  // Shadow Map Configuration (eliminate shadow acne with positive bias)
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  // Set up Cameras, Lighting, and Event Handlers
  createCameras();
  setupLighting();
  setupEventListeners();

  // Load the 3D City GLB Model
  loadCityModel();

  // Begin Render Loop
  animate();
}

function cacheDOMElements() {
  dom = {
    canvas: document.getElementById('city-canvas'),
    loadingOverlay: document.getElementById('loading-overlay'),
    loadingText: document.getElementById('loading-text'),
    loadingBar: document.getElementById('loading-bar'),
    errorOverlay: document.getElementById('error-overlay'),
    errorMessage: document.getElementById('error-message'),
    statusProjection: document.getElementById('projection-mode'),
    statusNav: document.getElementById('nav-status'),
    statusCamY: document.getElementById('cam-y-display'),
    statusCamPos: document.getElementById('cam-pos-display'),
    statusHSR: document.getElementById('hsr-display'),
    fpsDisplay: document.getElementById('fps-display'),
    btnStartNav: document.getElementById('btn-start-nav'),
    btnResetView: document.getElementById('btn-reset-view'),
    btnToggleProjection: document.getElementById('btn-toggle-projection'),
    btnEnableVisibility: document.getElementById('btn-enable-visibility'),
    visibilityResult: document.getElementById('visibility-result'),
    visTargetName: document.getElementById('vis-target-name'),
    visDistance: document.getElementById('vis-distance'),
    visResultText: document.getElementById('vis-result-text'),
    crosshair: document.getElementById('crosshair'),
  };
}

// =================================================================
// 3. CAMERAS (Perspective & Orthographic)
// =================================================================

function createCameras() {
  const aspect = window.innerWidth / window.innerHeight;

  // 1. Perspective Camera — used for both Overview and First-Person Walk
  perspectiveCamera = new THREE.PerspectiveCamera(55, aspect, 0.1, 4000);
  perspectiveCamera.position.copy(overviewCameraPosition);
  perspectiveCamera.lookAt(overviewCameraTarget);

  // 2. Orthographic Camera — technical, architectural overview
  const initialFrustum = 800;
  orthographicCamera = new THREE.OrthographicCamera(
    -initialFrustum * aspect / 2,
    initialFrustum * aspect / 2,
    initialFrustum / 2,
    -initialFrustum / 2,
    1.0,
    5000
  );
  orthographicCamera.position.set(0, 550, 0);
  orthographicCamera.lookAt(0, 0, 0);

  // Default active camera
  activeCamera = perspectiveCamera;
  isPerspective = true;
  updateStatusDisplay();
}

function updateOrthographicFrustum() {
  const aspect = window.innerWidth / window.innerHeight;
  // Fit both X (721m) and Z (607m) city dimensions with 15% padding
  const padding = 1.15;
  const extentZ = (citySize.z > 0 ? citySize.z : 620) * padding;
  const extentX = (citySize.x > 0 ? citySize.x : 740) * padding;

  // Frustum height H must be at least extentZ, and H * aspect must be at least extentX
  const frustumH = Math.max(extentZ, extentX / aspect);
  const frustumW = frustumH * aspect;

  orthographicCamera.top = frustumH / 2;
  orthographicCamera.bottom = -frustumH / 2;
  orthographicCamera.left = -frustumW / 2;
  orthographicCamera.right = frustumW / 2;
  orthographicCamera.updateProjectionMatrix();
}

// =================================================================
// 4. BALANCED SCENE LIGHTING & SHADOW SETUP
// =================================================================

let sunLight, sunTarget, fillLight, hemiLight, ambientLight;

function setupLighting() {
  // Ambient Light — base illumination ensuring shadowed surfaces are never pitch black
  ambientLight = new THREE.AmbientLight(0xffffff, 0.35);
  scene.add(ambientLight);

  // Hemisphere Light — sky blue top, warm ground reflection bottom
  hemiLight = new THREE.HemisphereLight(0xddeeff, 0x554433, 0.85);
  hemiLight.position.set(0, 300, 0);
  scene.add(hemiLight);

  // Primary Directional Sun Light — creates crisp shadows and architectural depth
  sunLight = new THREE.DirectionalLight(0xfff6ea, 1.8);
  sunLight.position.set(280, 420, 220);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 2048;
  sunLight.shadow.mapSize.height = 2048;
  sunLight.shadow.camera.near = 10;
  sunLight.shadow.camera.far = 1400;

  // Shadow camera bounds tailored to Manhattan city dimensions
  const d = 420;
  sunLight.shadow.camera.left = -d;
  sunLight.shadow.camera.right = d;
  sunLight.shadow.camera.top = d;
  sunLight.shadow.camera.bottom = -d;
  // Use positive normal bias to completely eliminate shadow acne
  sunLight.shadow.bias = 0.0005;
  sunLight.shadow.normalBias = 0.02;

  sunTarget = new THREE.Object3D();
  sunTarget.position.set(0, 0, 0);
  scene.add(sunTarget);
  sunLight.target = sunTarget;
  scene.add(sunLight);

  // Secondary Sky Fill Light — illuminates opposite sides of buildings
  fillLight = new THREE.DirectionalLight(0x99bbdd, 0.7);
  fillLight.position.set(-250, 300, -250);
  scene.add(fillLight);
}

// =================================================================
// 5. MATERIAL ARCHITECTURE & PROCEDURAL TEXTURE GENERATION
// =================================================================

// Cache procedural building facade textures
const textureCache = new Map();

/**
 * Generates an architectural window grid texture matching Blender's intended Brick Texture.
 * Because UVs are scaled as U = length / 2.2m and V = height / 3.6m, RepeatWrapping creates
 * realistic window columns and floor rows across all building faces.
 */
function getBuildingFacadeTexture(wallHex, glassHex, litHex, isGlassTower) {
  const cacheKey = `${wallHex}_${glassHex}_${litHex}_${isGlassTower}`;
  if (textureCache.has(cacheKey)) {
    return textureCache.get(cacheKey);
  }

  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');

  // Fill wall / mortar frame
  ctx.fillStyle = wallHex;
  ctx.fillRect(0, 0, 128, 128);

  const cols = 2;
  const rows = 2;
  const padX = isGlassTower ? 6 : 14;
  const padY = isGlassTower ? 8 : 12;
  const paneW = (128 - padX * (cols + 1)) / cols;
  const paneH = (128 - padY * (rows + 1)) / rows;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = padX + c * (paneW + padX);
      const y = padY + r * (paneH + padY);

      // Vary lit vs unlit office windows
      const isLit = (c + r) % 2 === 0;
      ctx.fillStyle = isLit ? litHex : glassHex;
      ctx.fillRect(x, y, paneW, paneH);

      // Subtle mullion / window frame edge
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.28)';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(x, y, paneW, paneH);

      // Diagonal glass reflection highlight
      ctx.fillStyle = 'rgba(255, 255, 255, 0.16)';
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + paneW * 0.45, y);
      ctx.lineTo(x, y + paneH * 0.45);
      ctx.closePath();
      ctx.fill();
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.colorSpace = THREE.SRGBColorSpace;

  textureCache.set(cacheKey, texture);
  return texture;
}

/**
 * Creates a paver sidewalk grid texture.
 */
function getSidewalkTexture() {
  if (textureCache.has('sidewalk')) return textureCache.get('sidewalk');

  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#b8b5af';
  ctx.fillRect(0, 0, 128, 128);

  ctx.strokeStyle = '#6e6c66';
  ctx.lineWidth = 2;
  ctx.strokeRect(4, 4, 120, 120);
  ctx.strokeRect(4, 4, 60, 60);
  ctx.strokeRect(64, 64, 60, 60);

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 4);
  texture.colorSpace = THREE.SRGBColorSpace;

  textureCache.set('sidewalk', texture);
  return texture;
}

/**
 * Complete PBR material definition map for all 31 materials in city.glb.
 * Resolves the black building surfaces by providing correct albedo, roughness,
 * metalness, and procedural facade textures.
 */
function createMaterialForName(name) {
  switch (name) {
    // 14 Architectural Facade Materials
    case 'Cobalt_Blue':
      return new THREE.MeshStandardMaterial({
        color: 0x1848bb,
        roughness: 0.22,
        metalness: 0.85,
        map: getBuildingFacadeTexture('#0a2e99', '#245ca8', '#4288d8', true),
      });

    case 'Cyan_Turquoise':
      return new THREE.MeshStandardMaterial({
        color: 0x1699aa,
        roughness: 0.18,
        metalness: 0.88,
        map: getBuildingFacadeTexture('#0d7a8c', '#186478', '#38b8cc', true),
      });

    case 'Dark_Navy':
      return new THREE.MeshStandardMaterial({
        color: 0x121a36,
        roughness: 0.20,
        metalness: 0.82,
        map: getBuildingFacadeTexture('#0c1328', '#1b3260', '#f5c66b', true),
      });

    case 'Emerald_Green':
      return new THREE.MeshStandardMaterial({
        color: 0x1a6b4a,
        roughness: 0.22,
        metalness: 0.85,
        map: getBuildingFacadeTexture('#105437', '#1c5e48', '#389a74', true),
      });

    case 'Silver_Steel':
      return new THREE.MeshStandardMaterial({
        color: 0xd0d8e2,
        roughness: 0.22,
        metalness: 0.92,
        map: getBuildingFacadeTexture('#b8c2ce', '#334c6e', '#5a84b8', true),
      });

    case 'Beige_Sandstone':
      return new THREE.MeshStandardMaterial({
        color: 0xd4ba96,
        roughness: 0.75,
        metalness: 0.05,
        map: getBuildingFacadeTexture('#c2a57e', '#232832', '#f0c266', false),
      });

    case 'Cream_Limestone':
      return new THREE.MeshStandardMaterial({
        color: 0xe5dfd2,
        roughness: 0.70,
        metalness: 0.05,
        map: getBuildingFacadeTexture('#d8d0c0', '#252d3a', '#ecc670', false),
      });

    case 'White_Marble':
      return new THREE.MeshStandardMaterial({
        color: 0xedeef2,
        roughness: 0.35,
        metalness: 0.12,
        map: getBuildingFacadeTexture('#dedfe5', '#24456b', '#4885bd', false),
      });

    case 'Granite_Gray':
      return new THREE.MeshStandardMaterial({
        color: 0x7a8088,
        roughness: 0.60,
        metalness: 0.15,
        map: getBuildingFacadeTexture('#6c727a', '#294868', '#506e8c', false),
      });

    case 'Classic_Red_Brick':
      return new THREE.MeshStandardMaterial({
        color: 0xa83828,
        roughness: 0.82,
        metalness: 0.02,
        map: getBuildingFacadeTexture('#902c1e', '#1c2024', '#f2b85c', false),
      });

    case 'Deep_Brown_Brick':
      return new THREE.MeshStandardMaterial({
        color: 0x623e2e,
        roughness: 0.82,
        metalness: 0.02,
        map: getBuildingFacadeTexture('#503123', '#201e1c', '#f0b556', false),
      });

    case 'Golden_Bronze':
      return new THREE.MeshStandardMaterial({
        color: 0xa47c4a,
        roughness: 0.26,
        metalness: 0.88,
        map: getBuildingFacadeTexture('#886438', '#382c1e', '#ba9052', true),
      });

    case 'Aqua_Sky_Glass':
      return new THREE.MeshStandardMaterial({
        color: 0x2b94dd,
        roughness: 0.18,
        metalness: 0.90,
        map: getBuildingFacadeTexture('#1e7ec0', '#1c3e60', '#56c2f8', true),
      });

    case 'Charcoal_Modern':
      return new THREE.MeshStandardMaterial({
        color: 0x2e3238,
        roughness: 0.40,
        metalness: 0.35,
        map: getBuildingFacadeTexture('#22252a', '#245a78', '#f2bc62', false),
      });

    // Ground-Level & Architectural Details
    case 'Storefront_Retail':
      return new THREE.MeshStandardMaterial({
        color: 0x363840,
        roughness: 0.25,
        metalness: 0.40,
        map: getBuildingFacadeTexture('#282a30', '#20344c', '#fed878', false),
      });

    case 'Roof_Gravel_Dark':
      return new THREE.MeshStandardMaterial({
        color: 0x2e3034,
        roughness: 0.88,
        metalness: 0.05,
      });

    case 'Metal_Dark_Steel':
      return new THREE.MeshStandardMaterial({
        color: 0x2a2d33,
        roughness: 0.35,
        metalness: 0.90,
      });

    case 'Metal_Galvanized_Chiller':
      return new THREE.MeshStandardMaterial({
        color: 0x9ba2a8,
        roughness: 0.30,
        metalness: 0.85,
      });

    case 'Wood_Water_Tank':
      return new THREE.MeshStandardMaterial({
        color: 0x78563a,
        roughness: 0.82,
        metalness: 0.0,
      });

    case 'Spire_Antenna':
      return new THREE.MeshStandardMaterial({
        color: 0xdde4ec,
        roughness: 0.18,
        metalness: 0.95,
      });

    // Streets, Sidewalks, & Road Markings
    case 'Asphalt_Road':
      return new THREE.MeshStandardMaterial({
        color: 0x222428,
        roughness: 0.85,
        metalness: 0.05,
      });

    case 'Concrete_Sidewalk':
      return new THREE.MeshStandardMaterial({
        color: 0xb5b2ab,
        roughness: 0.78,
        metalness: 0.05,
        map: getSidewalkTexture(),
      });

    case 'Road_Marking_White':
      return new THREE.MeshStandardMaterial({
        color: 0xf0f0f0,
        roughness: 0.35,
        metalness: 0.0,
      });

    case 'Road_Marking_Yellow':
      return new THREE.MeshStandardMaterial({
        color: 0xf5be18,
        roughness: 0.35,
        metalness: 0.0,
      });

    // Street Furniture & Trees
    case 'Lamp_Metal':
      return new THREE.MeshStandardMaterial({
        color: 0x202428,
        roughness: 0.35,
        metalness: 0.85,
      });

    case 'Lamp_Light':
      return new THREE.MeshStandardMaterial({
        color: 0xfff3d0,
        emissive: new THREE.Color(0xffeaad),
        emissiveIntensity: 3.5,
        roughness: 0.1,
      });

    case 'Tree_Grate_CastIron':
      return new THREE.MeshStandardMaterial({
        color: 0x26272a,
        roughness: 0.65,
        metalness: 0.80,
      });

    case 'Hydrant_Red':
      return new THREE.MeshStandardMaterial({
        color: 0xd92620,
        roughness: 0.32,
        metalness: 0.25,
      });

    case 'Tree_Bark':
      return new THREE.MeshStandardMaterial({
        color: 0x483222,
        roughness: 0.90,
        metalness: 0.0,
      });

    case 'Tree_Leaves':
      return new THREE.MeshStandardMaterial({
        color: 0x287834,
        roughness: 0.55,
        metalness: 0.0,
        side: THREE.DoubleSide, // Leaves rendered on both sides
      });

    case 'Tree_Leaves_Light':
      return new THREE.MeshStandardMaterial({
        color: 0x3e9444,
        roughness: 0.50,
        metalness: 0.0,
        side: THREE.DoubleSide,
      });

    default:
      // Fallback for any unnamed mesh
      return new THREE.MeshStandardMaterial({
        color: 0x9098a4,
        roughness: 0.5,
        metalness: 0.2,
      });
  }
}

// =================================================================
// 6. MODEL LOADING & SCENE SETUP
// =================================================================

function loadCityModel() {
  const loader = new GLTFLoader();

  loader.load(
    '/city.glb',

    function onLoad(gltf) {
      cityModel = gltf.scene;

      obstacleMeshes.length = 0;

      // Inspect every mesh, repair materials, and configure shadows
      cityModel.traverse(function (child) {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;

          // Repair material if missing/unlit/black
          const currentMat = child.material;
          if (currentMat) {
            const matName = currentMat.name;
            const repairedMat = createMaterialForName(matName);

            // Ensure depth testing (HSR) is enabled
            repairedMat.depthTest = true;
            repairedMat.depthWrite = true;

            // Preserve single-sided rendering for all architectural solids
            if (matName !== 'Tree_Leaves' && matName !== 'Tree_Leaves_Light') {
              repairedMat.side = THREE.FrontSide;
            }

            child.material = repairedMat;

            // Classify obstacles for collision detection
            const isGround = matName === 'Asphalt_Road' ||
              matName === 'Road_Marking_White' ||
              matName === 'Road_Marking_Yellow' ||
              matName === 'Concrete_Sidewalk';

            if (!isGround) {
              child.userData.isObstacle = true;
              obstacleMeshes.push(child);
            }
          }
        }
      });

      scene.add(cityModel);

      // Compute exact model bounds
      cityBoundingBox.setFromObject(cityModel);
      cityBoundingBox.getCenter(cityCenter);
      cityBoundingBox.getSize(citySize);

      console.log('Manhattan City loaded successfully.');
      console.log('Dimensions (X, Y, Z):', citySize);
      console.log('Center:', cityCenter);

      // Update orthographic camera frustum to encompass entire city
      updateOrthographicFrustum();

      // Configure overview camera position to frame the entire skyline
      const maxDim = Math.max(citySize.x, citySize.z);
      overviewCameraPosition.set(maxDim * 0.58, citySize.y * 1.35, maxDim * 0.65);
      overviewCameraTarget.set(cityCenter.x, citySize.y * 0.25, cityCenter.z);

      perspectiveCamera.position.copy(overviewCameraPosition);
      perspectiveCamera.lookAt(overviewCameraTarget);

      // Fade out loading overlay
      dom.loadingOverlay.style.transition = 'opacity 0.4s ease';
      dom.loadingOverlay.style.opacity = '0';
      setTimeout(function () {
        dom.loadingOverlay.style.display = 'none';
      }, 400);

      updateStatusDisplay();
    },

    function onProgress(event) {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        dom.loadingText.textContent = `Loading Manhattan City Model… ${percent}%`;
        dom.loadingBar.style.width = `${percent}%`;
      }
    },

    function onError(error) {
      console.error('GLTF loading error:', error);
      dom.loadingOverlay.style.display = 'none';
      dom.errorMessage.textContent = `Failed to load city.glb: ${error.message || 'Check public/city.glb'}`;
      dom.errorOverlay.style.display = 'flex';
    }
  );
}

// =================================================================
// 7. EVENT LISTENERS & RESIZE
// =================================================================

function setupEventListeners() {
  window.addEventListener('resize', onWindowResize);

  dom.btnStartNav.addEventListener('click', enterFirstPersonNavigation);
  dom.btnResetView.addEventListener('click', resetToOverview);
  dom.btnToggleProjection.addEventListener('click', toggleProjection);
  dom.btnEnableVisibility.addEventListener('click', toggleVisibilityMode);

  // Keyboard controls
  window.addEventListener('keydown', function (e) {
    keysPressed[e.code] = true;

    // Hotkey: 'E' to test line-of-sight while in navigation
    if (e.code === 'KeyE') {
      testForwardVisibility();
    }
  });

  window.addEventListener('keyup', function (e) {
    keysPressed[e.code] = false;
  });

  // Mouse look via Pointer Lock
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('pointerlockchange', onPointerLockChange);

  // Canvas click for visibility test
  dom.canvas.addEventListener('click', onCanvasClick);
}

function onWindowResize() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  const aspect = width / height;

  perspectiveCamera.aspect = aspect;
  perspectiveCamera.updateProjectionMatrix();

  updateOrthographicFrustum();

  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}

// =================================================================
// 8. FIRST-PERSON STREET NAVIGATION
// =================================================================

function enterFirstPersonNavigation() {
  // Ensure we are in perspective mode
  if (!isPerspective) {
    toggleProjection();
  }

  isFirstPersonNav = true;

  // Set camera to verified open avenue intersection
  perspectiveCamera.position.copy(streetStartPosition);
  perspectiveCamera.fov = 70; // wider immersive walking FOV
  perspectiveCamera.updateProjectionMatrix();

  // Face toward the central skyscraper core
  yaw = streetStartFacingYaw;
  pitch = 0.05; // slight upward gaze at towers
  const euler = new THREE.Euler(pitch, yaw, 0, 'YXZ');
  perspectiveCamera.quaternion.setFromEuler(euler);

  // Request pointer lock for mouse look
  dom.canvas.requestPointerLock();
}

function resetToOverview() {
  if (document.pointerLockElement === dom.canvas) {
    document.exitPointerLock();
  }

  isFirstPersonNav = false;

  // Restore overview vantage point
  perspectiveCamera.fov = 55;
  perspectiveCamera.updateProjectionMatrix();
  perspectiveCamera.position.copy(overviewCameraPosition);
  perspectiveCamera.lookAt(overviewCameraTarget);

  clearVisibilityVisualization();
  updateStatusDisplay();
}

function onPointerLockChange() {
  if (document.pointerLockElement === dom.canvas) {
    isFirstPersonNav = true;
    document.body.classList.add('navigating');
    dom.crosshair.style.display = 'block';
    dom.btnStartNav.textContent = '● Walking in First-Person';
  } else {
    document.body.classList.remove('navigating');
    dom.crosshair.style.display = 'none';
    dom.btnStartNav.textContent = '▶ Start First-Person Walk';
  }
  updateStatusDisplay();
}

function onMouseMove(event) {
  if (document.pointerLockElement !== dom.canvas) return;

  yaw -= event.movementX * LOOK_SENSITIVITY;
  pitch -= event.movementY * LOOK_SENSITIVITY;

  // Clamp vertical pitch to prevent gimbal flip (±85 degrees)
  const maxPitch = Math.PI / 2 - 0.06;
  pitch = Math.max(-maxPitch, Math.min(maxPitch, pitch));

  const euler = new THREE.Euler(pitch, yaw, 0, 'YXZ');
  perspectiveCamera.quaternion.setFromEuler(euler);
}

// Vectors allocated once to avoid garbage collection spikes in render loop
const moveForward = new THREE.Vector3();
const moveRight = new THREE.Vector3();
const proposedStep = new THREE.Vector3();
const colRaycaster = new THREE.Raycaster();
const colOrigin = new THREE.Vector3();
const colDir = new THREE.Vector3();

function processMovement(deltaTime) {
  if (!isFirstPersonNav || document.pointerLockElement !== dom.canvas) return;

  const dt = Math.min(deltaTime, 0.1);

  // Horizontal movement vectors based solely on yaw (no vertical flying)
  moveForward.set(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
  moveRight.set(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

  const isSprinting = keysPressed['ShiftLeft'] || keysPressed['ShiftRight'];
  const speed = WALK_SPEED * (isSprinting ? SPRINT_MULTIPLIER : 1.0) * dt;

  let moveX = 0;
  let moveZ = 0;

  if (keysPressed['KeyW']) {
    moveX += moveForward.x * speed;
    moveZ += moveForward.z * speed;
  }
  if (keysPressed['KeyS']) {
    moveX -= moveForward.x * speed;
    moveZ -= moveForward.z * speed;
  }
  if (keysPressed['KeyA']) {
    moveX -= moveRight.x * speed;
    moveZ -= moveRight.z * speed;
  }
  if (keysPressed['KeyD']) {
    moveX += moveRight.x * speed;
    moveZ += moveRight.z * speed;
  }

  if (moveX === 0 && moveZ === 0) return;

  // Slide-collision detection: test X and Z independently to allow smooth wall sliding
  const currentPos = perspectiveCamera.position;

  // Test X-axis movement
  if (moveX !== 0) {
    if (canMoveInDirection(currentPos, Math.sign(moveX), 0, Math.abs(moveX))) {
      currentPos.x += moveX;
    }
  }

  // Test Z-axis movement
  if (moveZ !== 0) {
    if (canMoveInDirection(currentPos, 0, Math.sign(moveZ), Math.abs(moveZ))) {
      currentPos.z += moveZ;
    }
  }
}

/**
 * Multi-height raycast check against building obstacles.
 * Prevents walking through walls while avoiding floor snagging.
 */
function canMoveInDirection(origin, dirX, dirZ, distance) {
  if (obstacleMeshes.length === 0) return true;

  colDir.set(dirX, 0, dirZ).normalize();
  const checkDist = distance + PLAYER_RADIUS;

  // Test at two heights: knee level (0.5m) and chest level (1.3m)
  const testHeights = [0.5, 1.3];
  for (let i = 0; i < testHeights.length; i++) {
    colOrigin.set(origin.x, (origin.y - EYE_HEIGHT) + testHeights[i], origin.z);
    colRaycaster.set(colOrigin, colDir);
    colRaycaster.far = checkDist;

    const hits = colRaycaster.intersectObjects(obstacleMeshes, false);
    if (hits.length > 0 && hits[0].distance < checkDist) {
      return false; // Obstacle detected
    }
  }

  return true;
}

// Ground raycast for smooth step-up onto curbs (0.18m)
const groundRaycaster = new THREE.Raycaster();
const groundOrigin = new THREE.Vector3();
const groundDir = new THREE.Vector3(0, -1, 0);

function maintainGroundHeight() {
  if (!isFirstPersonNav || !cityModel) return;

  const camPos = perspectiveCamera.position;
  groundOrigin.set(camPos.x, camPos.y + 1.0, camPos.z);
  groundRaycaster.set(groundOrigin, groundDir);
  groundRaycaster.far = 10.0;

  const hits = groundRaycaster.intersectObject(cityModel, true);

  if (hits.length > 0) {
    // Find highest ground surface under player
    let groundY = 0;
    for (let i = 0; i < hits.length; i++) {
      if (hits[i].point.y <= camPos.y + 0.5) {
        groundY = Math.max(groundY, hits[i].point.y);
      }
    }

    const targetCamY = groundY + EYE_HEIGHT;
    // Smooth lerp (no snapping)
    camPos.y += (targetCamY - camPos.y) * 0.25;
  } else {
    // Safety clamp: keep player at street level if stepping off edge
    camPos.y = Math.max(camPos.y, EYE_HEIGHT);
  }
}

// =================================================================
// 9. PROJECTION TOGGLING (Perspective ↔ Orthographic)
// =================================================================

function toggleProjection() {
  // Exit first-person navigation before switching to orthographic
  if (document.pointerLockElement === dom.canvas) {
    document.exitPointerLock();
  }

  isPerspective = !isPerspective;

  if (isPerspective) {
    activeCamera = perspectiveCamera;
    dom.statusProjection.textContent = 'Perspective';
    dom.btnToggleProjection.textContent = 'Toggle Projection (Switch to Ortho)';
  } else {
    updateOrthographicFrustum();
    activeCamera = orthographicCamera;
    dom.statusProjection.textContent = 'Orthographic';
    dom.btnToggleProjection.textContent = 'Toggle Projection (Switch to Persp)';
  }

  updateStatusDisplay();
}

// =================================================================
// 10. VISIBILITY ANALYSIS (Raycast Line-of-Sight & HSR)
// =================================================================

function toggleVisibilityMode() {
  visibilityModeActive = !visibilityModeActive;

  if (visibilityModeActive) {
    dom.btnEnableVisibility.textContent = '🎯 Visibility Mode: ON';
    dom.btnEnableVisibility.classList.add('btn-active');
  } else {
    dom.btnEnableVisibility.textContent = '🎯 Visibility Mode: OFF';
    dom.btnEnableVisibility.classList.remove('btn-active');
    clearVisibilityVisualization();
  }
}

const clickRaycaster = new THREE.Raycaster();
const clickNDC = new THREE.Vector2();

function onCanvasClick(event) {
  if (!visibilityModeActive || document.pointerLockElement === dom.canvas || !cityModel) return;

  clickNDC.x = (event.clientX / window.innerWidth) * 2 - 1;
  clickNDC.y = -(event.clientY / window.innerHeight) * 2 + 1;

  clickRaycaster.setFromCamera(clickNDC, activeCamera);
  const hits = clickRaycaster.intersectObject(cityModel, true);

  if (hits.length === 0) return;

  const targetPoint = hits[0].point;
  const targetMesh = hits[0].object;
  performLineOfSightTest(activeCamera.position, targetPoint, targetMesh);
}

/**
 * Tests line-of-sight directly in front of the crosshair while walking.
 */
function testForwardVisibility() {
  if (!cityModel) return;

  const ray = new THREE.Raycaster();
  ray.set(perspectiveCamera.position, perspectiveCamera.getWorldDirection(new THREE.Vector3()));
  ray.far = 1200;

  const hits = ray.intersectObject(cityModel, true);
  if (hits.length === 0) return;

  const targetPoint = hits[0].point;
  const targetMesh = hits[0].object;
  performLineOfSightTest(perspectiveCamera.position, targetPoint, targetMesh);
}

function performLineOfSightTest(fromPos, toPos, targetMesh) {
  const dir = new THREE.Vector3().subVectors(toPos, fromPos);
  const distance = dir.length();
  dir.normalize();

  // Offset ray origin slightly forward so it doesn't self-intersect observer
  const origin = fromPos.clone().addScaledVector(dir, 0.5);

  const losRay = new THREE.Raycaster(origin, dir, 0.1, distance + 1.0);
  const hits = losRay.intersectObject(cityModel, true);

  let isVisible = false;
  let hitName = targetMesh.name || targetMesh.parent?.name || 'Building';

  if (hits.length > 0) {
    const firstHit = hits[0];
    const distDiff = Math.abs(firstHit.distance - (distance - 0.5));
    // If first hit is the target object or within 1.0m tolerance
    if (distDiff < 1.0 || firstHit.object === targetMesh) {
      isVisible = true;
    } else {
      hitName = firstHit.object.name || 'Obstacle';
    }
  }

  // Update UI Result
  dom.visTargetName.textContent = targetMesh.name || 'Building';
  dom.visDistance.textContent = `${distance.toFixed(1)} m`;

  if (isVisible) {
    dom.visResultText.textContent = '✅ VISIBLE (Direct Line of Sight)';
    dom.visResultText.className = 'vis-visible';
  } else {
    dom.visResultText.textContent = `❌ OCCLUDED (Blocked by ${hitName})`;
    dom.visResultText.className = 'vis-occluded';
  }

  drawVisibilityRay(fromPos, toPos, isVisible);
}

function drawVisibilityRay(from, to, isVisible) {
  clearVisibilityVisualization();

  const color = isVisible ? 0x10b981 : 0xef4444;

  const lineGeo = new THREE.BufferGeometry().setFromPoints([from, to]);
  const lineMat = new THREE.LineBasicMaterial({
    color: color,
    linewidth: 3,
    depthTest: false,
  });
  visRayLine = new THREE.Line(lineGeo, lineMat);
  visRayLine.renderOrder = 999;
  scene.add(visRayLine);

  const markerGeo = new THREE.SphereGeometry(1.5, 16, 16);
  const markerMat = new THREE.MeshBasicMaterial({
    color: color,
    depthTest: false,
  });
  visTargetMarker = new THREE.Mesh(markerGeo, markerMat);
  visTargetMarker.position.copy(to);
  visTargetMarker.renderOrder = 999;
  scene.add(visTargetMarker);
}

function clearVisibilityVisualization() {
  if (visRayLine) {
    visRayLine.geometry.dispose();
    visRayLine.material.dispose();
    scene.remove(visRayLine);
    visRayLine = null;
  }
  if (visTargetMarker) {
    visTargetMarker.geometry.dispose();
    visTargetMarker.material.dispose();
    scene.remove(visTargetMarker);
    visTargetMarker = null;
  }
}

// =================================================================
// 11. STATUS PANEL UPDATES & RENDER LOOP
// =================================================================

function updateStatusDisplay() {
  if (dom.statusCamY) {
    dom.statusCamY.textContent = `${activeCamera.position.y.toFixed(2)} m`;
  }
  if (dom.statusCamPos) {
    dom.statusCamPos.textContent = `X: ${activeCamera.position.x.toFixed(0)} | Z: ${activeCamera.position.z.toFixed(0)}`;
  }
  if (dom.statusNav) {
    dom.statusNav.textContent = isFirstPersonNav ? 'First-Person Walk' : 'City Overview';
    dom.statusNav.style.color = isFirstPersonNav ? '#34d399' : '#e2e8f0';
  }
}

function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();

  // Process movement & collision in first-person mode
  processMovement(deltaTime);
  maintainGroundHeight();

  // Update status metrics
  updateStatusDisplay();

  // FPS calculation
  frameCount++;
  const now = performance.now();
  if (now - lastFpsTime >= 1000) {
    dom.fpsDisplay.textContent = frameCount;
    frameCount = 0;
    lastFpsTime = now;
  }

  // Render with Depth Buffer (Hidden Surface Removal)
  renderer.render(scene, activeCamera);
}

// Initialize Application
init();
