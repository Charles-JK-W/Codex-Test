const telemetryData = [
  {
    timestamp: '2024-04-12T09:20:00Z',
    depth: 45,
    heading: 132,
    speed: 2.4,
    battery: 96,
    temperature: 12.4,
    pressure: 2.8,
  },
  {
    timestamp: '2024-04-12T09:21:00Z',
    depth: 48,
    heading: 140,
    speed: 2.6,
    battery: 95,
    temperature: 12.5,
    pressure: 2.95,
  },
  {
    timestamp: '2024-04-12T09:22:00Z',
    depth: 52,
    heading: 145,
    speed: 2.2,
    battery: 94,
    temperature: 12.6,
    pressure: 3.1,
  },
  {
    timestamp: '2024-04-12T09:23:00Z',
    depth: 55,
    heading: 150,
    speed: 2.1,
    battery: 92,
    temperature: 12.8,
    pressure: 3.3,
  },
  {
    timestamp: '2024-04-12T09:24:00Z',
    depth: 58,
    heading: 152,
    speed: 1.9,
    battery: 91,
    temperature: 13,
    pressure: 3.45,
  },
  {
    timestamp: '2024-04-12T09:25:00Z',
    depth: 60,
    heading: 149,
    speed: 1.8,
    battery: 90,
    temperature: 13.2,
    pressure: 3.6,
  },
  {
    timestamp: '2024-04-12T09:26:00Z',
    depth: 62,
    heading: 148,
    speed: 1.7,
    battery: 89,
    temperature: 13.4,
    pressure: 3.7,
  },
  {
    timestamp: '2024-04-12T09:27:00Z',
    depth: 61,
    heading: 146,
    speed: 1.6,
    battery: 89,
    temperature: 13.6,
    pressure: 3.8,
  },
  {
    timestamp: '2024-04-12T09:28:00Z',
    depth: 63,
    heading: 143,
    speed: 1.8,
    battery: 88,
    temperature: 13.7,
    pressure: 3.9,
  },
  {
    timestamp: '2024-04-12T09:29:00Z',
    depth: 65,
    heading: 140,
    speed: 1.7,
    battery: 87,
    temperature: 13.9,
    pressure: 4,
  },
];

function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

function populateStatus(data) {
  const latest = data[data.length - 1];
  document.getElementById('depth-value').textContent = latest.depth;
  document.getElementById('heading-value').textContent = latest.heading;
  document.getElementById('speed-value').textContent = latest.speed.toFixed(1);
  document.getElementById('battery-value').textContent = latest.battery;
  document.getElementById('last-updated').textContent = new Date(
    latest.timestamp
  ).toLocaleString();
}

function populateTelemetryTable(data) {
  const tbody = document.getElementById('telemetry-body');
  tbody.innerHTML = '';

  data
    .slice()
    .reverse()
    .forEach((entry) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${formatTime(entry.timestamp)}</td>
        <td>${entry.depth}</td>
        <td>${entry.heading}</td>
        <td>${entry.speed.toFixed(1)}</td>
        <td>${entry.battery}</td>
      `;
      tbody.appendChild(row);
    });
}

function renderDepthChart(ctx, data) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map((entry) => formatTime(entry.timestamp)),
      datasets: [
        {
          label: 'Depth (m)',
          data: data.map((entry) => entry.depth),
          tension: 0.35,
          fill: {
            target: 'origin',
            above: 'rgba(56, 189, 248, 0.25)',
          },
          borderColor: '#38bdf8',
          borderWidth: 3,
          pointRadius: 3,
          pointBackgroundColor: '#38bdf8',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          ticks: { color: 'rgba(226, 232, 240, 0.7)' },
          grid: { color: 'rgba(148, 163, 184, 0.2)' },
          title: { display: true, text: 'Meters' },
        },
        x: {
          ticks: { color: 'rgba(226, 232, 240, 0.7)' },
          grid: { color: 'rgba(148, 163, 184, 0.15)' },
        },
      },
      plugins: {
        legend: {
          labels: { color: 'rgba(226, 232, 240, 0.8)' },
        },
      },
    },
  });
}

function renderEnvironmentChart(ctx, data) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map((entry) => formatTime(entry.timestamp)),
      datasets: [
        {
          label: 'Temperature (°C)',
          data: data.map((entry) => entry.temperature),
          borderColor: '#fbbf24',
          backgroundColor: 'rgba(251, 191, 36, 0.15)',
          tension: 0.3,
          fill: true,
          borderWidth: 2,
        },
        {
          label: 'Pressure (MPa)',
          data: data.map((entry) => entry.pressure),
          borderColor: '#818cf8',
          backgroundColor: 'rgba(129, 140, 248, 0.2)',
          tension: 0.3,
          fill: true,
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          ticks: { color: 'rgba(226, 232, 240, 0.7)' },
          grid: { color: 'rgba(148, 163, 184, 0.2)' },
        },
        x: {
          ticks: { color: 'rgba(226, 232, 240, 0.7)' },
          grid: { color: 'rgba(148, 163, 184, 0.15)' },
        },
      },
      plugins: {
        legend: {
          labels: { color: 'rgba(226, 232, 240, 0.8)' },
        },
      },
    },
  });
}

function initDashboard() {
  populateStatus(telemetryData);
  populateTelemetryTable(telemetryData);

  const depthCtx = document.getElementById('depth-chart');
  const envCtx = document.getElementById('environment-chart');

  renderDepthChart(depthCtx, telemetryData);
  renderEnvironmentChart(envCtx, telemetryData);
}

document.addEventListener('DOMContentLoaded', initDashboard);
