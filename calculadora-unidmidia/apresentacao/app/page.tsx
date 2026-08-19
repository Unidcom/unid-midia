"use client";

import { useEffect, useMemo, useState } from "react";

type Media = { id: string; name: string; city: "Umuarama" | "Cianorte" | "Goioere"; type: "Outdoor" | "Painel LED" | "Busdoor" | "Trade"; price: number; unit: string; note: string; image?: string };

const media: Media[] = [
  { id: "out-um", name: "Outdoor 9 x 3 m", city: "Umuarama", type: "Outdoor", price: 490, unit: "bi-semana", note: "28 pontos catalogados" },
  { id: "bus-um", name: "Busdoor", city: "Umuarama", type: "Busdoor", price: 650, unit: "carro / mes", note: "Instalacao: R$ 550 por carro" },
  { id: "super-led", name: "Super Tela Av. Parana", city: "Umuarama", type: "Painel LED", price: 1250, unit: "face / mes", note: "270+ insercoes por dia" },
  { id: "leblon", name: "Painel LED Posto Leblon", city: "Umuarama", type: "Painel LED", price: 690, unit: "mes", note: "250 insercoes por dia" },
  { id: "avenida", name: "Painel LED Posto Avenida", city: "Umuarama", type: "Painel LED", price: 590, unit: "mes", note: "Av. Brasil com Av. Ipiranga" },
  { id: "itamaraty", name: "Painel LED Posto Itamaraty", city: "Umuarama", type: "Painel LED", price: 590, unit: "mes", note: "Av. Parana com Av. Apucarana" },
  { id: "makio", name: "Front com Iluminacao", city: "Cianorte", type: "Outdoor", price: 1100, unit: "mes", note: "Av. Makio Sato, Atlantico - entrando", image: "/media/outdoor-cianorte-1.jpeg" },
  { id: "espirito", name: "Front com Iluminacao", city: "Cianorte", type: "Outdoor", price: 1300, unit: "mes", note: "Av. Espirito Santo com Av. Allan Kardec", image: "/media/outdoor-cianorte-2.jpeg" },
  { id: "trade-go", name: "Pacote Trade Parana", city: "Goioere", type: "Trade", price: 25000, unit: "60 dias", note: "Producao, instalacao e retirada inclusas" },
];

const slides = ["Panorama", "Pracas", "Inventario", "Composicao", "Proposta"];
const currency = (value: number) => new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 }).format(value);

export default function Home() {
  const [slide, setSlide] = useState(0);
  const [city, setCity] = useState<Media["city"]>("Umuarama");
  const [selectedId, setSelectedId] = useState("out-um");
  const [period, setPeriod] = useState(1);
  const [quantity, setQuantity] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const selected = media.find((item) => item.id === selectedId) ?? media[0];
  const cityItems = useMemo(() => media.filter((item) => item.city === city), [city]);
  const total = selected.price * period * quantity;
  const go = (next: number) => setSlide(Math.min(Math.max(next, 0), slides.length - 1));

  function chooseCity(nextCity: Media["city"]) { setCity(nextCity); const first = media.find((item) => item.city === nextCity); if (first) setSelectedId(first.id); }
  async function toggleFullscreen() { if (!document.fullscreenElement) await document.documentElement.requestFullscreen(); else await document.exitFullscreen(); }

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => { if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") { event.preventDefault(); go(slide + 1); } if (event.key === "ArrowLeft" || event.key === "PageUp") { event.preventDefault(); go(slide - 1); } if (event.key === "Home") go(0); if (event.key === "End") go(slides.length - 1); };
    const onFullscreen = () => setIsFullscreen(Boolean(document.fullscreenElement));
    window.addEventListener("keydown", onKeyDown); document.addEventListener("fullscreenchange", onFullscreen);
    return () => { window.removeEventListener("keydown", onKeyDown); document.removeEventListener("fullscreenchange", onFullscreen); };
  }, [slide]);

  return <main className="deck-shell"><div className="deck" aria-live="polite">
    <section className={`slide cover ${slide === 0 ? "active" : ""}`}><div className="cover-overlay" /><div className="cover-copy"><p className="eyebrow light">UNID MIDIA · APRESENTACAO COMERCIAL</p><h1>Presenca que<br />vira escolha.</h1><p className="lead">Uma forma clara de desenhar cobertura, selecionar midias e chegar a uma proposta que faz sentido para cada praca.</p><div className="cover-stats"><span>3 cidades</span><span>4 formatos</span><span>valores organizados</span></div></div><div className="cover-bottom"><span>Plano de midia exterior</span><span>2026</span></div></section>
    <section className={`slide light-slide ${slide === 1 ? "active" : ""}`}><div className="section-top"><p className="eyebrow">01 · PRACAS</p><span>Escolha por territorio</span></div><div className="two-col city-layout"><div><h2>A conversa comeca pela cidade.</h2><p className="body-copy">A apresentacao muda junto com a necessidade do cliente. Selecione a praca para revelar o inventario que importa.</p><div className="segmented" role="group" aria-label="Cidade selecionada">{(["Umuarama", "Cianorte", "Goioere"] as const).map((item) => <button key={item} className={city === item ? "selected" : ""} onClick={() => chooseCity(item)}>{item}</button>)}</div><div className="city-note"><strong>{cityItems.length} midias</strong><span>disponiveis na base para {city}.</span></div></div><div className="city-visual"><div className="city-map"><span className="map-dot one" /><span className="map-dot two" /><span className="map-dot three" /><span className="map-route route-a" /><span className="map-route route-b" /><b>{city}</b></div><p>Comece por onde a campanha precisa ser vista. Depois, escolha a combinacao de alcance e frequencia.</p></div></div></section>
    <section className={`slide dark-slide ${slide === 2 ? "active" : ""}`}><div className="section-top inverted"><p className="eyebrow">02 · INVENTARIO</p><span>O que pode entrar na proposta</span></div><div className="inventory-head"><h2>{city} em foco.</h2><p>Itens ativos, com unidade de cobranca transparente.</p></div><div className="media-grid">{cityItems.map((item) => <button className={`media-card ${selectedId === item.id ? "selected" : ""}`} key={item.id} onClick={() => setSelectedId(item.id)}>{item.image && <img src={item.image} alt="Ponto de outdoor em Cianorte" />}<div className="media-card-body"><span className="tag">{item.type}</span><h3>{item.name}</h3><p>{item.note}</p><div><strong>{currency(item.price)}</strong><span> / {item.unit}</span></div></div></button>)}</div></section>
    <section className={`slide light-slide ${slide === 3 ? "active" : ""}`}><div className="section-top"><p className="eyebrow">03 · COMPOSICAO</p><span>Simulacao em reuniao</span></div><div className="calculator-layout"><div className="calculator-main"><h2>Monte o cenario ao vivo.</h2><p className="body-copy">A selecao preserva a conversa comercial: uma midia, um periodo e uma quantidade claros antes de fechar a proposta.</p><label className="field-label" htmlFor="media-select">Midia</label><select id="media-select" value={selectedId} onChange={(event) => { const next = media.find((item) => item.id === event.target.value); if (next) { setSelectedId(next.id); setCity(next.city); } }}>{media.map((item) => <option value={item.id} key={item.id}>{item.city} · {item.name}</option>)}</select><div className="control-row"><div><span className="field-label">Periodo</span><div className="segmented compact">{[1, 3, 12].map((value) => <button key={value} className={period === value ? "selected" : ""} onClick={() => setPeriod(value)}>{value} {value === 1 ? "mes" : "meses"}</button>)}</div></div><div><span className="field-label">Quantidade</span><div className="stepper"><button aria-label="Diminuir quantidade" onClick={() => setQuantity(Math.max(1, quantity - 1))}>−</button><b>{quantity}</b><button aria-label="Aumentar quantidade" onClick={() => setQuantity(quantity + 1)}>+</button></div></div></div></div><aside className="price-panel"><span className="tag amber">RESUMO</span><p>{selected.city} · {selected.type}</p><h3>{selected.name}</h3><div className="total">{currency(total)}</div><small>{quantity} x {currency(selected.price)} por {selected.unit} · {period} {period === 1 ? "mes" : "meses"}</small><div className="rule" /><span className="muted">Itens adicionais como VT, lona ou instalacao entram na etapa final da proposta.</span></aside></div></section>
    <section className={`slide finale ${slide === 4 ? "active" : ""}`}><div className="finale-copy"><p className="eyebrow">04 · PROPOSTA</p><h2>Uma proposta clara<br />e defendida no detalhe.</h2><p className="body-copy">A calculadora se torna um roteiro comercial: praca, inventario, investimento e condicoes reunidos em uma unica conversa.</p><div className="proposal-list"><span>01 · Objetivo de cobertura</span><span>02 · Midias e pontos selecionados</span><span>03 · Investimento e adicionais</span><span>04 · Proximos passos</span></div></div><div className="finale-art"><div className="art-ring ring-a" /><div className="art-ring ring-b" /><div className="art-card"><span>UNID MIDIA</span><strong>{currency(total)}</strong><small>cenario atual</small></div></div></section>
  </div><nav className="deck-controls" aria-label="Controles da apresentacao"><button className="icon-button" onClick={() => go(slide - 1)} disabled={slide === 0} aria-label="Slide anterior" title="Slide anterior">←</button><div className="progress-wrap"><span>{String(slide + 1).padStart(2, "0")} / {String(slides.length).padStart(2, "0")}</span><div className="progress"><i style={{ width: `${((slide + 1) / slides.length) * 100}%` }} /></div></div><div className="control-actions"><button className="icon-button" onClick={toggleFullscreen} aria-label={isFullscreen ? "Sair da tela cheia" : "Tela cheia"} title={isFullscreen ? "Sair da tela cheia" : "Tela cheia"}>{isFullscreen ? "×" : "⛶"}</button><button className="icon-button" onClick={() => window.print()} aria-label="Exportar para PDF" title="Exportar para PDF">↧</button><button className="icon-button" onClick={() => go(slide + 1)} disabled={slide === slides.length - 1} aria-label="Proximo slide" title="Proximo slide">→</button></div></nav></main>;
}
