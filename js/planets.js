// 행성 소개 페이지: 필터, 카드, 상세 모달
(function () {
  const grid = document.getElementById("grid");
  const modal = document.getElementById("modal");
  const fmt = (n) => n.toLocaleString("ko-KR");

  function render(filter) {
    const list = filter === "all" ? PLANETS : PLANETS.filter((p) => p.type === filter);
    grid.innerHTML = list.map((p, i) => `
      <button class="card" style="--c:${p.color};animation-delay:${i * 60}ms" data-id="${p.id}">
        <div class="pic"><img src="${p.img}" alt="${p.name} 사진" loading="lazy"></div>
        <div class="body">
          <h3>${p.name}<small>${p.en}</small></h3>
          <span class="tag">${p.type}</span>
          <p>지름 ${fmt(p.diameter)}km · 위성 ${p.moons}</p>
        </div>
      </button>`).join("");
  }

  function open(id, updateHash = true) {
    const p = PLANETS.find((x) => x.id === id);
    if (!p) return;
    document.getElementById("m-img").src = p.img;
    document.getElementById("m-img").alt = p.name + " 사진";
    document.getElementById("m-title").textContent = `${p.name} (${p.en})`;
    const tag = document.getElementById("m-tag");
    tag.textContent = p.type;
    tag.style.setProperty("--c", p.color);
    document.getElementById("m-desc").textContent = p.desc;
    document.getElementById("m-fact").textContent = "💡 " + p.fact;
    document.getElementById("m-info").innerHTML = `
      <dt>지름</dt><dd>${fmt(p.diameter)} km</dd>
      <dt>태양까지 거리</dt><dd>${p.au} AU (약 ${fmt(p.mkm)}백만 km)</dd>
      <dt>공전 주기</dt><dd>${p.orbit}</dd>
      <dt>자전 주기</dt><dd>${p.rotation}</dd>
      <dt>위성</dt><dd>${p.moons}</dd>
      <dt>온도</dt><dd>${p.temp}</dd>
      <dt>표면 중력</dt><dd>${p.gravity} m/s²</dd>`;
    if (!modal.open) modal.showModal();
    if (updateHash) history.replaceState(null, "", "#" + id);
  }

  document.querySelectorAll(".filters button").forEach((b) =>
    b.addEventListener("click", () => {
      document.querySelectorAll(".filters button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      render(b.dataset.filter);
    })
  );

  grid.addEventListener("click", (e) => {
    const card = e.target.closest(".card");
    if (card) open(card.dataset.id);
  });

  modal.querySelector(".close").addEventListener("click", () => modal.close());
  modal.addEventListener("click", (e) => { if (e.target === modal) modal.close(); });
  modal.addEventListener("close", () => history.replaceState(null, "", location.pathname));

  render("all");
  if (location.hash) open(location.hash.slice(1), false); // 홈에서 넘어온 링크
})();
