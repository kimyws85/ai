// 공통: 별 배경, 스크롤 등장 효과, 푸터 이미지 출처
(function () {
  // 별 생성
  const layer = document.createElement("div");
  layer.id = "stars";
  layer.setAttribute("aria-hidden", "true");
  for (let i = 0; i < 110; i++) {
    const s = document.createElement("i");
    s.style.left = Math.random() * 100 + "%";
    s.style.top = Math.random() * 100 + "%";
    s.style.setProperty("--d", 2 + Math.random() * 4 + "s");
    s.style.setProperty("--dl", Math.random() * 4 + "s");
    layer.appendChild(s);
  }
  document.body.prepend(layer);

  // 스크롤 시 등장
  const items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("show"); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    items.forEach((el) => io.observe(el));
  } else {
    items.forEach((el) => el.classList.add("show"));
  }

  // 이미지 출처 (Wikimedia Commons 파일 페이지)
  const credits = [
    ["태양", "The_Sun_in_white_light.jpg"],
    ["수성", "Mercury_in_true_color.jpg"],
    ["금성", "Venus_from_Mariner_10.jpg"],
    ["지구", "Meteosat-12-fci-march-equinox-2025-noon.jpg"],
    ["화성 (Kevin M. Gill)", "Mars_-_August_30_2021_-_Flickr_-_Kevin_M._Gill.png"],
    ["목성", "Jupiter_OPAL_2024.png"],
    ["토성", "Saturn_global_view_from_Cassini,_rings_open_Better_Colour.png"],
    ["천왕성", "Uranus_Voyager2_color_calibrated.png"],
    ["해왕성", "Neptune_Voyager2_color_calibrated.png"]
  ];
  const slot = document.getElementById("credits");
  if (slot) {
    const list = credits.map(([n, f]) =>
      `<li>${n}: <a href="https://commons.wikimedia.org/wiki/File:${encodeURIComponent(f)}" target="_blank" rel="noopener">${f.replace(/_/g, " ")}</a></li>`
    ).join("");
    slot.innerHTML = `<details><summary>이미지 출처 (Wikimedia Commons)</summary><ul>${list}</ul>
      <p style="margin-top:8px">각 이미지의 저작자와 이용 조건은 위 파일 페이지에서 확인할 수 있습니다.</p></details>`;
  }
})();
