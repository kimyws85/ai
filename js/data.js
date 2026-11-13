// 태양계 행성 데이터 (공개 천문 자료 기준, 근삿값)
const PLANETS = [
  {
    id: "mercury", name: "수성", en: "Mercury", type: "암석형", img: "images/mercury.jpg", color: "#9c9288",
    diameter: 4879, au: 0.39, mkm: 57.9, orbit: "88일", orbitDays: 88, rotation: "58.6일", moons: "0개",
    temp: "평균 167°C", gravity: 3.7,
    desc: "태양에서 가장 가깝고 태양계에서 가장 작은 행성입니다. 대기가 거의 없어 낮에는 400°C 넘게 오르고 밤에는 영하 170°C 아래로 떨어집니다.",
    fact: "수성의 하루(태양일)는 약 176지구일로, 1년(88일)보다 깁니다."
  },
  {
    id: "venus", name: "금성", en: "Venus", type: "암석형", img: "images/venus.jpg", color: "#d9b27a",
    diameter: 12104, au: 0.72, mkm: 108.2, orbit: "224.7일", orbitDays: 224.7, rotation: "243일 (역방향)", moons: "0개",
    temp: "평균 464°C", gravity: 8.87,
    desc: "크기가 지구와 비슷해 '쌍둥이 행성'으로 불리지만, 두꺼운 이산화탄소 대기의 온실효과로 태양계에서 가장 뜨겁습니다. 표면 기압은 지구의 약 90배입니다.",
    fact: "금성은 대부분의 행성과 반대 방향으로 자전해서 태양이 서쪽에서 뜹니다."
  },
  {
    id: "earth", name: "지구", en: "Earth", type: "암석형", img: "images/earth.jpg", color: "#4f8fd8",
    diameter: 12742, au: 1.0, mkm: 149.6, orbit: "365.25일", orbitDays: 365.25, rotation: "23시간 56분", moons: "1개",
    temp: "평균 15°C", gravity: 9.81,
    desc: "지금까지 생명이 확인된 유일한 행성입니다. 표면의 약 71%가 바닷물로 덮여 있고, 질소와 산소가 중심인 대기가 생명체를 보호합니다.",
    fact: "지구는 태양계 암석형 행성 중 가장 크고 밀도가 가장 높습니다."
  },
  {
    id: "mars", name: "화성", en: "Mars", type: "암석형", img: "images/mars.png", color: "#c8643c",
    diameter: 6779, au: 1.52, mkm: 227.9, orbit: "687일", orbitDays: 687, rotation: "24시간 37분", moons: "2개",
    temp: "평균 -65°C", gravity: 3.71,
    desc: "산화철 때문에 붉게 보이는 행성입니다. 태양계에서 가장 큰 화산인 올림포스 산과 거대한 협곡 마리너리스 계곡이 있습니다.",
    fact: "올림포스 산의 높이는 약 21.9km로 에베레스트 산의 두 배가 넘습니다."
  },
  {
    id: "jupiter", name: "목성", en: "Jupiter", type: "가스 행성", img: "images/jupiter.png", color: "#d6a77a",
    diameter: 139820, au: 5.2, mkm: 778.5, orbit: "11.86년", orbitDays: 4332.6, rotation: "9시간 56분", moons: "95개 이상",
    temp: "구름 꼭대기 약 -110°C", gravity: 24.79,
    desc: "태양계에서 가장 큰 행성으로, 다른 모든 행성을 합친 질량의 2배가 넘습니다. 대적점은 수백 년 이상 이어지는 거대한 폭풍입니다.",
    fact: "목성의 자전 주기는 태양계 행성 중 가장 짧아 하루가 10시간도 안 됩니다."
  },
  {
    id: "saturn", name: "토성", en: "Saturn", type: "가스 행성", img: "images/saturn.png", color: "#e3cd9b",
    diameter: 116460, au: 9.58, mkm: 1434, orbit: "29.4년", orbitDays: 10759, rotation: "10시간 34분", moons: "140개 이상",
    temp: "구름 꼭대기 약 -140°C", gravity: 10.44,
    desc: "얼음과 암석 조각으로 이루어진 화려한 고리로 유명합니다. 평균 밀도가 물보다 낮아, 아주 큰 물통이 있다면 물에 뜰 수 있습니다.",
    fact: "토성의 고리는 지름이 수십만 km에 이르지만 두께는 대부분 10m 안팎으로 매우 얇습니다."
  },
  {
    id: "uranus", name: "천왕성", en: "Uranus", type: "얼음 거인", img: "images/uranus.png", color: "#9fd8dc",
    diameter: 50724, au: 19.2, mkm: 2871, orbit: "84년", orbitDays: 30687, rotation: "17시간 14분 (역방향)", moons: "28개",
    temp: "구름 꼭대기 약 -195°C", gravity: 8.69,
    desc: "메탄 때문에 청록색으로 보이는 얼음 거인입니다. 자전축이 약 98° 기울어, 옆으로 누워서 공전하는 것처럼 보입니다.",
    fact: "천왕성은 1781년 윌리엄 허셜이 망원경으로 발견한 최초의 행성입니다."
  },
  {
    id: "neptune", name: "해왕성", en: "Neptune", type: "얼음 거인", img: "images/neptune.png", color: "#4a6fe0",
    diameter: 49244, au: 30.05, mkm: 4495, orbit: "164.8년", orbitDays: 60190, rotation: "16시간 6분", moons: "16개",
    temp: "구름 꼭대기 약 -200°C", gravity: 11.15,
    desc: "태양에서 가장 먼 행성으로, 태양계에서 가장 강한 바람(시속 2,000km 안팎)이 붑니다. 1846년 관측이 아닌 수학적 계산으로 위치가 예측된 뒤 발견되었습니다.",
    fact: "해왕성은 1846년 발견된 이후 태양을 겨우 한 바퀴 돌았습니다(2011년)."
  }
];

const SUN = { name: "태양", en: "Sun", img: "images/sun.jpg", diameter: 1392700 };
