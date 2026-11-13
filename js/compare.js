// 비교 페이지: 막대 그래프(스크롤 시 애니메이션), 눈금 전환, 정렬 가능한 표
(function () {
  const fmt = (n) => n.toLocaleString("ko-KR");
  const sizeBox = document.getElementById("size-bars");
  const distBox = document.getElementById("dist-bars");

  function rows(box, items) {
    box.innerHTML = items.map((it) => `
      <div class="bar-row" style="--c:${it.color}">
        <span>${it.name}</span>
        <div class="bar-track"><div class="bar" data-w="${it.w}"></div></div>
        <span class="val">${it.label}</span>
      </div>`).join("");
  }

  function grow(box) {
    // 한 프레임 뒤에 너비를 적용해야 전환 애니메이션이 재생됨
    requestAnimationFrame(() => requestAnimationFrame(() =>
      box.querySelectorAll(".bar").forEach((b) => (b.style.width = b.dataset.w + "%"))
    ));
  }

  // 지름: 목성 = 100%, 태양 포함
  const maxD = Math.max(...PLANETS.map((p) => p.diameter));
  rows(sizeBox, [
    { name: SUN.name, color: "#ffb347", w: 100, label: `${(SUN.diameter / maxD).toFixed(1)}배` },
    ...PLANETS.map((p) => ({
      name: p.name, color: p.color,
      w: Math.max((p.diameter / maxD) * 100, 1.5), label: fmt(p.diameter) + "km"
    }))
  ]);
  // 태양 막대는 목성의 10배라 가득 채워서 표시하고 라벨로 배수를 알려 줌
  // 거리
  function drawDist(scale, animate = true) {
    const maxAU = Math.max(...PLANETS.map((p) => p.au));
    const val = (au) => scale === "log" ? Math.log10(au * 10) / Math.log10(maxAU * 10) : au / maxAU;
    rows(distBox, PLANETS.map((p) => ({
      name: p.name, color: p.color, w: Math.max(val(p.au) * 100, 1.5), label: `${p.au} AU`
    })));
    if (animate) grow(distBox);
  }

  document.querySelectorAll(".toggle button").forEach((b) =>
    b.addEventListener("click", () => {
      document.querySelectorAll(".toggle button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      drawDist(b.dataset.scale);
    })
  );

  // 화면에 보일 때 막대 애니메이션 시작
  drawDist("linear", false); // 첫 그리기는 화면에 보일 때 재생
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { grow(e.target); io.unobserve(e.target); }
    });
  }, { threshold: 0.25 });
  io.observe(sizeBox);
  io.observe(distBox);

  // 표
  const tbody = document.querySelector("#tbl tbody");
  let sortKey = null, dir = 1;
  function drawTable() {
    const list = [...PLANETS];
    if (sortKey) {
      list.sort((a, b) => (a[sortKey] > b[sortKey] ? 1 : a[sortKey] < b[sortKey] ? -1 : 0) * dir);
    }
    tbody.innerHTML = list.map((p) => `
      <tr style="--c:${p.color}">
        <td><span class="swatch"></span>${p.name}</td><td>${p.type}</td>
        <td>${fmt(p.diameter)}</td><td>${p.au}</td><td>${p.orbit}</td><td>${p.gravity}</td>
      </tr>`).join("");
  }
  document.querySelectorAll("#tbl th").forEach((th) =>
    th.addEventListener("click", () => {
      const key = th.dataset.key;
      dir = sortKey === key ? -dir : 1;
      sortKey = key;
      document.querySelectorAll("#tbl th").forEach((x) => x.removeAttribute("data-dir"));
      th.dataset.dir = dir === 1 ? "asc" : "desc";
      drawTable();
    })
  );
  drawTable();
})();
