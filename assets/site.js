'use strict';
const menu_button = document.querySelector('.menu');
const sidebar = document.querySelector('.sidebar');
function close_menu() { sidebar.classList.remove('open'); menu_button.setAttribute('aria-expanded', 'false'); }
menu_button?.addEventListener('click', () => { const is_open = sidebar.classList.toggle('open'); menu_button.setAttribute('aria-expanded', String(is_open)); });
document.addEventListener('keydown', (event) => { if (event.key === 'Escape') close_menu(); });
document.addEventListener('click', (event) => { if (!sidebar.contains(event.target) && !menu_button.contains(event.target)) close_menu(); });

// Grayscale field with a bright region: all displayed numbers are actual pixels.
const brightness = document.querySelector('#brightness');
if (brightness) {
  const canvas = document.querySelector('#pixel-canvas');
  const context = canvas.getContext('2d');
  const grid = document.querySelector('#pixel-matrix');
  function render_pixels() {
    const gain = Number(brightness.value) / 100;
    grid.replaceChildren();
    for (let y = 0; y < 8; y++) {
      for (let x = 0; x < 8; x++) {
        const radius = Math.hypot(x - 3.1, y - 3.7);
        const base = radius < 2.65 ? 170 + x * 8 - y * 10 : 30 + x * 3 + y * 2;
        const value = Math.max(0, Math.min(255, Math.round(base * gain)));
        context.fillStyle = `rgb(${value},${value},${value})`;
        context.fillRect(x * 32, y * 32, 32, 32);
        const cell = document.createElement('span');
        cell.textContent = value;
        cell.style.background = context.fillStyle;
        cell.style.color = value > 145 ? '#15213a' : '#fff';
        grid.append(cell);
      }
    }
    document.querySelector('#brightness-value').textContent = gain.toFixed(2);
  }
  brightness.addEventListener('input', render_pixels);
  render_pixels();
}

const convolution = document.querySelector('#conv-position');
if (convolution) {
  const input_values = [[0,0,1,1,1],[0,0,1,1,1],[0,0,1,1,1],[0,0,1,1,1],[0,0,1,1,1]];
  const kernel = [[-1,0,1],[-1,0,1],[-1,0,1]];
  function render_convolution() {
    const index = Number(convolution.value), row = Math.floor(index / 3), col = index % 3;
    const input_grid = document.querySelector('#conv-input');
    const output_grid = document.querySelector('#conv-output');
    input_grid.replaceChildren(); output_grid.replaceChildren();
    input_values.flat().forEach((value, i) => {
      const y = Math.floor(i / 5), x = i % 5;
      const cell = document.createElement('span'); cell.textContent = value;
      const active = y >= row && y < row + 3 && x >= col && x < col + 3;
      cell.style.background = active ? '#2454d8' : '#edf2fa'; cell.style.color = active ? '#fff' : '#607089';
      input_grid.append(cell);
    });
    let chosen = 0;
    for (let y = 0; y < 3; y++) for (let x = 0; x < 3; x++) {
      let sum = 0;
      for (let ky = 0; ky < 3; ky++) for (let kx = 0; kx < 3; kx++) sum += input_values[y + ky][x + kx] * kernel[ky][kx];
      const cell = document.createElement('span'); cell.textContent = sum;
      cell.style.background = '#e7f2ef'; cell.style.color = '#08796f';
      if (y === row && x === col) { cell.classList.add('selected'); chosen = sum; }
      output_grid.append(cell);
    }
    document.querySelector('#conv-value').textContent = `위치 (${row}, ${col}) · 곱한 값 9개의 합 = ${chosen}`;
  }
  convolution.addEventListener('input', render_convolution); render_convolution();
}

const patch_size = document.querySelector('#patch-size');
if (patch_size) {
  const canvas = document.querySelector('#patch-canvas'), context = canvas.getContext('2d');
  function render_patches() {
    const patch = Number(patch_size.value), side = 224, n = side / patch, count = n * n;
    for (let y = 0; y < side; y++) for (let x = 0; x < side; x++) {
      const value = 45 + Math.round(140 * Math.exp(-((x - 105) ** 2 + (y - 110) ** 2) / 4900));
      context.fillStyle = `rgb(${value - 20},${value + 15},${Math.min(255, value + 65)})`; context.fillRect(x, y, 1, 1);
    }
    context.strokeStyle = '#fff'; context.lineWidth = .9;
    for (let position = 0; position <= side; position += patch) {
      context.beginPath(); context.moveTo(position, 0); context.lineTo(position, side); context.stroke();
      context.beginPath(); context.moveTo(0, position); context.lineTo(side, position); context.stroke();
    }
    document.querySelector('#patch-result').innerHTML = `<b>${n} × ${n} = ${count} patches</b><br>패치 벡터: ${patch} × ${patch} × 3 = ${patch * patch * 3}<br>CLS 포함: [B, ${count + 1}, 768]<br>head당 score 원소: ${(count + 1) ** 2}`;
  }
  patch_size.addEventListener('change', render_patches); render_patches();
}

const threshold = document.querySelector('#threshold');
if (threshold) {
  // A fixed teaching dataset, not measured production performance.
  const samples = [{y:1,p:.95},{y:1,p:.86},{y:1,p:.73},{y:1,p:.64},{y:1,p:.44},{y:0,p:.79},{y:0,p:.57},{y:0,p:.32},{y:0,p:.22},{y:0,p:.09}];
  function render_metrics() {
    const limit = Number(threshold.value) / 100;
    let tp = 0, fp = 0, tn = 0, fn = 0;
    samples.forEach(({y,p}) => { if (p >= limit) { if (y) tp++; else fp++; } else { if (y) fn++; else tn++; } });
    const precision = tp + fp ? tp / (tp + fp) : null;
    const recall = tp / (tp + fn), f1 = 2 * tp / (2 * tp + fp + fn);
    document.querySelector('#threshold-value').textContent = limit.toFixed(2);
    for (const [id, value] of Object.entries({tp,fp,tn,fn})) document.querySelector(`#${id}`).textContent = value;
    document.querySelector('#precision').textContent = precision === null ? '정의 안 됨' : precision.toFixed(3);
    document.querySelector('#recall').textContent = recall.toFixed(3);
    document.querySelector('#f1').textContent = f1.toFixed(3);
  }
  threshold.addEventListener('input', render_metrics); render_metrics();
}
