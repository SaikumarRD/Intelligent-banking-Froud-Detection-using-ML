/* ═══════════════════════════════════════════════════
   Sentinel AI — Dashboard Script
   Three.js 3D scene  ·  Flask API integration  ·  UI
   ═══════════════════════════════════════════════════ */

const API = (window.location.protocol.startsWith('http')) ? window.location.origin : 'http://127.0.0.1:5000';

/* ─── Embedded fallback data (used when Flask is offline) ─── */
const FALLBACK_META = {
    metrics: {
        "Logistic Regression":      { accuracy:99.52, precision:80.65, recall:100, f1:89.29, roc_auc:0.9999, tn:9752, fp:48, fn:0, tp:200 },
        "Decision Tree":            { accuracy:99.97, precision:99.50, recall:99,  f1:99.25, roc_auc:0.9949, tn:9799, fp:1,  fn:2, tp:198 },
        "Random Forest":            { accuracy:99.98, precision:99.01, recall:100, f1:99.50, roc_auc:1.0,    tn:9798, fp:2,  fn:0, tp:200 },
        "Support Vector Machine":   { accuracy:99.68, precision:86.21, recall:100, f1:92.59, roc_auc:0.9999, tn:9768, fp:32, fn:0, tp:200 }
    },
    top_features: [
        { Feature:"RiskScore",           Importance:49.76 },
        { Feature:"LoginAttempts",       Importance:21.33 },
        { Feature:"TransactionHour",     Importance:13.71 },
        { Feature:"TransactionDuration", Importance:3.82  },
        { Feature:"TransactionAmount",   Importance:3.11  },
        { Feature:"AccountBalance",      Importance:2.43  },
        { Feature:"DayOfWeek",           Importance:1.49  },
        { Feature:"IsWeekend",           Importance:1.18  },
        { Feature:"CustomerAge",         Importance:1.12  },
        { Feature:"Channel_Branch",      Importance:0.58  }
    ],
    total_records:50000,
    fraud_count:1000,
    legit_count:49000
};

let META = null;   // will be set after fetch or fallback

/* ═══════════════════════════════════════
   1.  THREE.JS BACKGROUND SCENE
   ═══════════════════════════════════════ */

function initScene() {
    if (typeof THREE === 'undefined') return;

    const canvas = document.getElementById('bg-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 30);

    /* ── Lights ── */
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.15);
    scene.add(ambientLight);

    const orangeLight = new THREE.PointLight(0xff6b00, 2.5, 80);
    orangeLight.position.set(12, 10, 15);
    scene.add(orangeLight);

    const greenLight = new THREE.PointLight(0x3ddc97, 1.8, 80);
    greenLight.position.set(-12, -8, 10);
    scene.add(greenLight);

    /* ── Central wireframe icosahedron ── */
    const icoGeo = new THREE.IcosahedronGeometry(5.5, 1);
    const icoMat = new THREE.MeshBasicMaterial({
        color: 0xff6b00,
        wireframe: true,
        transparent: true,
        opacity: 0.18
    });
    const ico = new THREE.Mesh(icoGeo, icoMat);
    scene.add(ico);

    /* ── Inner glowing sphere ── */
    const glowGeo = new THREE.SphereGeometry(3.2, 32, 32);
    const glowMat = new THREE.MeshStandardMaterial({
        color: 0xff6b00,
        emissive: 0xff6b00,
        emissiveIntensity: 0.35,
        transparent: true,
        opacity: 0.12,
        roughness: 0.4,
        metalness: 0.3
    });
    const glow = new THREE.Mesh(glowGeo, glowMat);
    scene.add(glow);

    /* ── Floating particles ── */
    const PARTICLE_COUNT = 600;
    const posArr = new Float32Array(PARTICLE_COUNT * 3);
    const colArr = new Float32Array(PARTICLE_COUNT * 3);
    const orange = new THREE.Color(0xff6b00);
    const green  = new THREE.Color(0x3ddc97);
    const amber  = new THREE.Color(0xf59e0b);

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        const i3 = i * 3;
        posArr[i3]     = (Math.random() - 0.5) * 80;
        posArr[i3 + 1] = (Math.random() - 0.5) * 80;
        posArr[i3 + 2] = (Math.random() - 0.5) * 80;
        const c = [orange, green, amber][Math.floor(Math.random() * 3)];
        colArr[i3]     = c.r;
        colArr[i3 + 1] = c.g;
        colArr[i3 + 2] = c.b;
    }
    const partGeo = new THREE.BufferGeometry();
    partGeo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
    partGeo.setAttribute('color',    new THREE.BufferAttribute(colArr, 3));
    const partMat = new THREE.PointsMaterial({
        size: 0.18,
        vertexColors: true,
        transparent: true,
        opacity: 0.7,
        sizeAttenuation: true
    });
    const particles = new THREE.Points(partGeo, partMat);
    scene.add(particles);

    /* ── Orbiting small octahedrons ── */
    const orbiters = [];
    for (let i = 0; i < 8; i++) {
        const geo = new THREE.OctahedronGeometry(0.25, 0);
        const mat = new THREE.MeshStandardMaterial({
            color: i % 2 === 0 ? 0xff6b00 : 0x3ddc97,
            emissive: i % 2 === 0 ? 0xff6b00 : 0x3ddc97,
            emissiveIntensity: 0.6,
            metalness: 0.5,
            roughness: 0.2
        });
        const mesh = new THREE.Mesh(geo, mat);
        const angle = (i / 8) * Math.PI * 2;
        const radius = 8 + Math.random() * 3;
        mesh.userData = { angle, radius, speed: 0.15 + Math.random() * 0.25, yOffset: (Math.random() - 0.5) * 6 };
        scene.add(mesh);
        orbiters.push(mesh);
    }

    /* ── Grid ring ── */
    const ringGeo = new THREE.RingGeometry(9, 9.08, 64);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xff6b00, transparent: true, opacity: 0.12, side: THREE.DoubleSide });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / 2;
    scene.add(ring);

    const ring2Geo = new THREE.RingGeometry(13, 13.06, 64);
    const ring2 = new THREE.Mesh(ring2Geo, ringMat.clone());
    ring2.material.opacity = 0.06;
    ring2.rotation.x = Math.PI / 2;
    scene.add(ring2);

    /* ── Mouse tracking ── */
    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth  - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    /* ── Resize ── */
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    /* ── Animation loop ── */
    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();

        // Central shape
        ico.rotation.x = t * 0.08;
        ico.rotation.y = t * 0.12;
        glow.rotation.y = -t * 0.06;

        // Rings
        ring.rotation.z = t * 0.05;
        ring2.rotation.z = -t * 0.03;

        // Particles slow drift
        const pPos = particles.geometry.attributes.position.array;
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            pPos[i * 3 + 1] += Math.sin(t * 0.3 + i) * 0.003;
        }
        particles.geometry.attributes.position.needsUpdate = true;
        particles.rotation.y = t * 0.015;

        // Orbiters
        orbiters.forEach(o => {
            const d = o.userData;
            d.angle += d.speed * 0.008;
            o.position.x = Math.cos(d.angle) * d.radius;
            o.position.z = Math.sin(d.angle) * d.radius;
            o.position.y = d.yOffset + Math.sin(t * 0.5 + d.angle) * 1.5;
            o.rotation.x = t * 0.5;
            o.rotation.z = t * 0.3;
        });

        // Camera follows mouse gently
        camera.position.x += (mouseX * 3 - camera.position.x) * 0.02;
        camera.position.y += (-mouseY * 2 - camera.position.y) * 0.02;
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
    }
    animate();
}

/* ═══════════════════════════════════════
   2.  MINI ORB (in-result-panel)
   ═══════════════════════════════════════ */

let orbScene, orbCamera, orbRenderer, orbSphere, orbMat;

function initOrb() {
    const canvas = document.getElementById('orb-canvas');
    if (!canvas || typeof THREE === 'undefined') return;

    orbRenderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    orbRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    orbRenderer.setSize(220, 220);

    orbScene = new THREE.Scene();
    orbCamera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    orbCamera.position.z = 4;

    orbScene.add(new THREE.AmbientLight(0xffffff, 0.5));
    const pl = new THREE.PointLight(0xff6b00, 2, 20);
    pl.position.set(3, 3, 5);
    orbScene.add(pl);

    const geo = new THREE.IcosahedronGeometry(1.2, 2);
    orbMat = new THREE.MeshStandardMaterial({
        color: 0x3ddc97,
        emissive: 0x3ddc97,
        emissiveIntensity: 0.4,
        metalness: 0.5,
        roughness: 0.3,
        wireframe: false
    });
    orbSphere = new THREE.Mesh(geo, orbMat);
    orbScene.add(orbSphere);

    const wireGeo = new THREE.IcosahedronGeometry(1.5, 1);
    const wireMat = new THREE.MeshBasicMaterial({ color: 0x3ddc97, wireframe: true, transparent: true, opacity: 0.15 });
    const wire = new THREE.Mesh(wireGeo, wireMat);
    orbScene.add(wire);

    function animOrb() {
        requestAnimationFrame(animOrb);
        const t = performance.now() * 0.001;
        orbSphere.rotation.x = t * 0.3;
        orbSphere.rotation.y = t * 0.5;
        wire.rotation.x = -t * 0.2;
        wire.rotation.y = -t * 0.35;
        orbRenderer.render(orbScene, orbCamera);
    }
    animOrb();
}

function setOrbColor(probability) {
    if (!orbMat) return;
    let color;
    if (probability < 0.25) color = new THREE.Color(0x3ddc97);       // green
    else if (probability < 0.65) color = new THREE.Color(0xf59e0b);  // amber
    else color = new THREE.Color(0xef4444);                          // red
    orbMat.color.copy(color);
    orbMat.emissive.copy(color);
}

/* ═══════════════════════════════════════
   3.  FETCH METADATA & POPULATE UI
   ═══════════════════════════════════════ */

async function loadMetadata() {
    try {
        const res = await fetch(API + '/api/metadata', { signal: AbortSignal.timeout(3000) });
        META = await res.json();
    } catch {
        META = FALLBACK_META;
    }
    populateOverview();
    populateModels();
    populateFeatures();
}

function populateOverview() {
    const m = META;
    document.getElementById('stat-total').textContent = m.total_records.toLocaleString();
    document.getElementById('stat-fraud-count').textContent = m.fraud_count.toLocaleString();
    const rate = ((m.fraud_count / m.total_records) * 100).toFixed(2);
    document.getElementById('stat-fraud-count').closest('.stat-card').querySelector('.stat-label').textContent = `Fraudulent (${rate}%)`;

    // Best model by F1
    let bestName = '', bestF1 = 0;
    for (const [name, v] of Object.entries(m.metrics)) {
        if (v.f1 > bestF1) { bestF1 = v.f1; bestName = name; }
    }
    document.getElementById('stat-champion').textContent = bestName;
    document.getElementById('stat-f1').textContent = bestF1.toFixed(2) + '%';
}

function populateModels() {
    const grid = document.getElementById('modelsGrid');
    grid.innerHTML = '';

    let bestName = '';
    let bestF1 = 0;
    for (const [name, v] of Object.entries(META.metrics)) {
        if (v.f1 > bestF1) { bestF1 = v.f1; bestName = name; }
    }

    for (const [name, v] of Object.entries(META.metrics)) {
        const isChamp = name === bestName;
        const card = document.createElement('div');
        card.className = 'model-card' + (isChamp ? ' champion' : '');
        card.innerHTML = `
            <div class="mc-name">${name}</div>
            ${isChamp ? '<span class="mc-badge">Champion</span>' : ''}
            <div class="mc-metrics">
                <div class="mc-metric"><span class="mc-val">${v.accuracy.toFixed(2)}%</span><span class="mc-lbl">Accuracy</span></div>
                <div class="mc-metric"><span class="mc-val">${v.precision.toFixed(2)}%</span><span class="mc-lbl">Precision</span></div>
                <div class="mc-metric"><span class="mc-val accent-green">${v.recall.toFixed(2)}%</span><span class="mc-lbl">Recall</span></div>
                <div class="mc-metric"><span class="mc-val accent-orange">${v.f1.toFixed(2)}%</span><span class="mc-lbl">F1‑Score</span></div>
            </div>
            <div class="mc-bar-wrap">
                <small style="font-size:.65rem;color:var(--text-muted)">ROC-AUC</small>
                <div class="mc-bar"><div class="mc-bar-fill" style="width:${v.roc_auc * 100}%"></div></div>
            </div>
            <div style="margin-top:.7rem;font-size:.72rem;color:var(--text-muted)">
                FP: ${v.fp} · FN: ${v.fn} · TP: ${v.tp} · TN: ${v.tn}
            </div>`;
        grid.appendChild(card);
    }
}

function populateFeatures() {
    const wrap = document.getElementById('featureBars');
    wrap.innerHTML = '';
    const sorted = [...META.top_features].sort((a, b) => b.Importance - a.Importance);
    const max = sorted[0].Importance;
    sorted.forEach(f => {
        const pct = (f.Importance / max * 100).toFixed(1);
        const row = document.createElement('div');
        row.className = 'feat-row';
        row.innerHTML = `
            <span class="feat-name">${f.Feature}</span>
            <div class="feat-bar-track"><div class="feat-bar-fill" style="width:${pct}%"></div></div>
            <span class="feat-pct">${f.Importance.toFixed(2)}%</span>`;
        wrap.appendChild(row);
    });
}

/* ═══════════════════════════════════════
   4.  LIVE DETECTOR — PREDICT
   ═══════════════════════════════════════ */

document.getElementById('predictForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        TransactionAmount:  parseFloat(document.getElementById('f-amount').value),
        AccountBalance:     parseFloat(document.getElementById('f-balance').value),
        TransactionDuration:parseFloat(document.getElementById('f-duration').value),
        CustomerAge:        parseInt(document.getElementById('f-age').value),
        RiskScore:          parseFloat(document.getElementById('f-risk').value),
        LoginAttempts:      parseInt(document.getElementById('f-login').value),
        TransactionType:    document.getElementById('f-type').value,
        Channel:            document.getElementById('f-channel').value,
        model_choice:       document.getElementById('f-model').value
    };

    document.getElementById('resultIdle').classList.add('hidden');
    const rd = document.getElementById('resultData');
    rd.classList.remove('hidden');

    try {
        const res = await fetch(API + '/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === 'success') {
            showResult(data);
        } else {
            showOfflineResult(payload);
        }
    } catch {
        showOfflineResult(payload);
    }
});

function showResult(d) {
    const badge = document.getElementById('resultBadge');
    badge.textContent = d.is_fraud ? '⛔ FRAUDULENT' : '✅ LEGITIMATE';
    badge.className = 'result-badge ' + (d.is_fraud ? 'fraud' : 'legit');

    document.getElementById('resultProb').textContent = d.fraud_probability.toFixed(2) + '%';
    document.getElementById('resultProb').style.color = d.is_fraud ? 'var(--red)' : 'var(--green)';
    document.getElementById('resultTier').textContent = d.prevention.tier;
    document.getElementById('resultAction').textContent = d.prevention.action;
    document.getElementById('resultAction').style.color = d.is_fraud ? 'var(--red)' : d.prevention.tier.includes('Medium') ? 'var(--amber)' : 'var(--green)';
    document.getElementById('resultDesc').textContent = d.prevention.description;

    setOrbColor(d.fraud_probability / 100);
}

function showOfflineResult(p) {
    // Simple heuristic when API is unreachable
    const risk = p.RiskScore / 100;
    const login = Math.min(p.LoginAttempts / 5, 1);
    const prob = Math.min(risk * 0.6 + login * 0.3 + (p.TransactionAmount > 8000 ? 0.1 : 0), 1);
    const isFraud = prob >= 0.5;

    const badge = document.getElementById('resultBadge');
    badge.textContent = isFraud ? '⛔ FRAUDULENT' : '✅ LEGITIMATE';
    badge.className = 'result-badge ' + (isFraud ? 'fraud' : 'legit');
    document.getElementById('resultProb').textContent = (prob * 100).toFixed(2) + '%';
    document.getElementById('resultProb').style.color = isFraud ? 'var(--red)' : 'var(--green)';

    let tier, action, desc;
    if (prob >= 0.65) {
        tier = 'Tier 3: High Risk'; action = 'AUTO-BLOCK & FREEZE'; desc = 'Transaction halted. Account locked.';
    } else if (prob >= 0.25) {
        tier = 'Tier 2: Medium Risk'; action = 'CHALLENGE 2FA / OTP'; desc = 'Step-up authentication required.';
    } else {
        tier = 'Tier 1: Low Risk'; action = 'AUTO-APPROVE'; desc = 'Instant verification. Authorized.';
    }
    document.getElementById('resultTier').textContent = tier + ' (offline estimate)';
    document.getElementById('resultAction').textContent = action;
    document.getElementById('resultAction').style.color = prob >= 0.65 ? 'var(--red)' : prob >= 0.25 ? 'var(--amber)' : 'var(--green)';
    document.getElementById('resultDesc').textContent = desc;

    setOrbColor(prob);
}

/* ═══════════════════════════════════════
   5.  BATCH CSV AUDIT
   ═══════════════════════════════════════ */

let selectedFile = null;
const csvInput = document.getElementById('csvFile');
const uploadZone = document.getElementById('uploadZone');
const auditBtn = document.getElementById('auditBtn');

csvInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        selectedFile = e.target.files[0];
        uploadZone.querySelector('p').textContent = '📄 ' + selectedFile.name;
        auditBtn.disabled = false;
    }
});

// Drag-and-drop
uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) {
        selectedFile = e.dataTransfer.files[0];
        uploadZone.querySelector('p').textContent = '📄 ' + selectedFile.name;
        auditBtn.disabled = false;
    }
});

auditBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    auditBtn.textContent = 'Analyzing…';
    auditBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('model_choice', document.getElementById('audit-model').value);

    try {
        const res = await fetch(API + '/api/upload', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.status === 'success') {
            showAuditResults(data);
        } else {
            alert('Audit error: ' + data.message);
        }
    } catch {
        alert('Could not reach the Flask server at ' + API + '. Make sure app.py is running.');
    }
    auditBtn.textContent = 'Run Audit';
    auditBtn.disabled = false;
});

function showAuditResults(d) {
    document.getElementById('auditSummary').classList.remove('hidden');
    document.getElementById('auditTableWrap').classList.remove('hidden');
    document.getElementById('a-total').textContent = d.total_processed;
    document.getElementById('a-fraud').textContent = d.fraud_detected;
    document.getElementById('a-legit').textContent = d.legitimate_count;
    document.getElementById('a-rate').textContent = d.fraud_rate + '%';

    const tbody = document.getElementById('auditTbody');
    tbody.innerHTML = '';
    d.records.forEach(r => {
        const tr = document.createElement('tr');
        const badgeCls = r.badge === 'danger' ? 'danger' : r.badge === 'success' ? 'success' : 'warning';
        tr.innerHTML = `
            <td>${r.id}</td>
            <td>${r.amount}</td>
            <td>${r.channel}</td>
            <td>${r.fraud_probability}</td>
            <td><span class="badge-sm ${r.is_fraud ? 'danger' : 'success'}">${r.is_fraud ? 'FRAUD' : 'OK'}</span></td>
            <td><span class="badge-sm ${badgeCls}">${r.action}</span></td>`;
        tbody.appendChild(tr);
    });
}

/* ═══════════════════════════════════════
   6.  SCROLL ANIMATIONS (IntersectionObserver)
   ═══════════════════════════════════════ */

function setupScrollAnimations() {
    const targets = document.querySelectorAll('.section, .stat-card, .model-card, .tier-card, .glass-panel');
    targets.forEach(el => el.classList.add('fade-in'));

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    targets.forEach(el => observer.observe(el));
}

/* ═══════════════════════════════════════
   7.  SMOOTH NAV HIGHLIGHT
   ═══════════════════════════════════════ */

function setupNavHighlight() {
    const links = document.querySelectorAll('.nav-links a');
    const sections = [...links].map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);

    function onScroll() {
        const scrollY = window.scrollY + 120;
        let current = '';
        sections.forEach(s => {
            if (s.offsetTop <= scrollY) current = '#' + s.id;
        });
        links.forEach(a => {
            a.style.color = a.getAttribute('href') === current ? 'var(--orange)' : '';
        });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
}

/* ═══════════════════════════════════════
   8.  BOOT
   ═══════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    initScene();
    initOrb();
    loadMetadata();
    setupScrollAnimations();
    setupNavHighlight();
});
