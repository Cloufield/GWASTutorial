(() => {
  const STORAGE_KEY = "gwastutorial.keyterms.hover.enabled";
  const BODY_ATTR = "data-keyterms-hover-enabled";
  const TOOLTIP_ID = "keyterms-hover-tooltip";
  const LINK_SELECTOR = "a[href*='cloufield.github.io/GWASDictionary/terms/'], a[href^='/terms/']";
  const CONTENT_SELECTOR = ".md-content__inner";

  function isEnabled() {
    const v = localStorage.getItem(STORAGE_KEY);
    return v === null ? false : v === "1";
  }

  function setEnabled(enabled) {
    localStorage.setItem(STORAGE_KEY, enabled ? "1" : "0");
    document.body.setAttribute(BODY_ATTR, enabled ? "1" : "0");
    const btn = document.getElementById("keyterms-hover-toggle");
    if (btn) {
      btn.setAttribute("aria-pressed", enabled ? "true" : "false");
      btn.setAttribute("title", enabled ? "Disable key term hover definitions" : "Enable key term hover definitions");
      btn.textContent = enabled ? "KT On" : "KT Off";
    }
  }

  function ensureTooltip() {
    let tip = document.getElementById(TOOLTIP_ID);
    if (!tip) {
      tip = document.createElement("div");
      tip.id = TOOLTIP_ID;
      tip.className = "keyterms-hover-tooltip";
      document.body.appendChild(tip);
    }
    return tip;
  }

  function moveTooltip(evt) {
    const tip = ensureTooltip();
    const x = Math.min(window.innerWidth - 320, evt.clientX + 14);
    const y = Math.min(window.innerHeight - 80, evt.clientY + 14);
    tip.style.left = `${Math.max(8, x)}px`;
    tip.style.top = `${Math.max(8, y)}px`;
  }

  function showTooltip(text, evt) {
    const tip = ensureTooltip();
    tip.textContent = text;
    tip.classList.add("is-visible");
    moveTooltip(evt);
  }

  function hideTooltip() {
    const tip = document.getElementById(TOOLTIP_ID);
    if (tip) tip.classList.remove("is-visible");
  }

  function extractDefinitionFromListItem(link) {
    const t = (link.getAttribute("title") || "").trim();
    if (t) return t;
    const li = link.closest("li");
    if (!li) return "";
    // Backward compatibility for old bullets formatted as: [Term] — definition
    const text = li.textContent || "";
    const parts = text.split(/[—–-]\s+/);
    if (parts.length < 2) return "";
    return parts.slice(1).join(" - ").trim();
  }

  function keyTermsSections() {
    const headings = Array.from(document.querySelectorAll(".md-content h2"));
    return headings.filter((h) => /key\s+terms/i.test((h.textContent || "").trim()));
  }

  function linksInSectionUntilNextH2(h2) {
    const links = [];
    let node = h2.nextElementSibling;
    while (node) {
      if (node.matches && node.matches("h2")) break;
      if (node.querySelectorAll) {
        node.querySelectorAll(LINK_SELECTOR).forEach((a) => links.push(a));
      }
      node = node.nextElementSibling;
    }
    return links;
  }

  function decorateKeyTermLink(link) {
    if (link.dataset.ktHoverBound === "1") return;
    const def = link.dataset.ktDefinition || extractDefinitionFromListItem(link);
    if (!def) return;
    link.dataset.ktDefinition = def;
    // Prevent the native browser title tooltip from duplicating our custom tooltip.
    if (link.hasAttribute("title")) link.removeAttribute("title");
    link.classList.add("keyterm-link");
    link.dataset.ktHoverBound = "1";
    link.addEventListener("mouseenter", (evt) => {
      if (document.body.getAttribute(BODY_ATTR) !== "1") return;
      showTooltip(def, evt);
    });
    link.addEventListener("mousemove", moveTooltip);
    link.addEventListener("mouseleave", hideTooltip);
    link.addEventListener("blur", hideTooltip);
  }

  function slugFromUrl(url) {
    const m = (url || "").match(/\/terms\/[^/]+\/([^/#?]+)\/?/);
    return m ? m[1] : "";
  }

  function aliasesFromLink(link, label) {
    const out = new Set();
    if (label) out.add(label.trim());
    const parenthetical = (label || "").match(/\(([^)]+)\)\s*$/);
    if (parenthetical && parenthetical[1]) out.add(parenthetical[1].trim());
    const slug = slugFromUrl(link.getAttribute("href") || "");
    if (slug) {
      if (/^[a-z]+$/.test(slug) && slug.length <= 8) out.add(slug.toUpperCase());
      const parts = slug.split("-").filter(Boolean);
      if (parts.length >= 2 && parts.length <= 8 && parts.every((p) => /^[a-z]+$/.test(p))) {
        out.add(parts.map((p) => p[0]).join("").toUpperCase());
      }
    }
    return Array.from(out).filter(Boolean);
  }

  function collectKeyTerms() {
    const terms = [];
    keyTermsSections().forEach((h2) => {
      linksInSectionUntilNextH2(h2).forEach((link) => {
        const def = extractDefinitionFromListItem(link);
        if (!def) return;
        link.dataset.ktDefinition = def;
        decorateKeyTermLink(link);
        terms.push({
          definition: def,
          variants: aliasesFromLink(link, (link.textContent || "").trim()),
        });
      });
    });
    return terms;
  }

  function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function decorateInlineTerm(node, definition) {
    if (!node || node.dataset.ktHoverBound === "1") return;
    node.classList.add("keyterm-link", "keyterm-inline");
    node.dataset.ktHoverBound = "1";
    node.dataset.ktDefinition = definition;
    node.addEventListener("mouseenter", (evt) => {
      if (document.body.getAttribute(BODY_ATTR) !== "1") return;
      showTooltip(definition, evt);
    });
    node.addEventListener("mousemove", moveTooltip);
    node.addEventListener("mouseleave", hideTooltip);
  }

  function applyInlineTerms(terms) {
    const root = document.querySelector(CONTENT_SELECTOR);
    if (!root || !terms.length) return;

    const variants = [];
    terms.forEach((t) => {
      t.variants.forEach((v) => {
        const vv = (v || "").trim();
        if (vv.length >= 2) variants.push({ term: vv, definition: t.definition });
      });
    });
    variants.sort((a, b) => b.term.length - a.term.length);
    if (!variants.length) return;

    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const p = node.parentElement;
        if (!p) return NodeFilter.FILTER_REJECT;
        if (p.closest("a, code, pre, kbd, samp, var, script, style, textarea, .md-header, .md-nav, .keyterm-inline")) {
          return NodeFilter.FILTER_REJECT;
        }
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);

    textNodes.forEach((textNode) => {
      const text = textNode.nodeValue || "";
      let start = 0;
      let changed = false;
      const frag = document.createDocumentFragment();

      while (start < text.length) {
        let best = null;
        for (const v of variants) {
          const re = new RegExp(`\\b${escapeRegExp(v.term)}\\b`, "i");
          const m = re.exec(text.slice(start));
          if (!m) continue;
          const idx = start + m.index;
          if (!best || idx < best.idx || (idx === best.idx && v.term.length > best.term.length)) {
            best = { idx, len: m[0].length, term: v.term, definition: v.definition };
          }
        }
        if (!best) break;
        if (best.idx > start) frag.appendChild(document.createTextNode(text.slice(start, best.idx)));
        const span = document.createElement("span");
        span.textContent = text.slice(best.idx, best.idx + best.len);
        decorateInlineTerm(span, best.definition);
        frag.appendChild(span);
        start = best.idx + best.len;
        changed = true;
      }

      if (!changed) return;
      if (start < text.length) frag.appendChild(document.createTextNode(text.slice(start)));
      textNode.parentNode.replaceChild(frag, textNode);
    });
  }

  function ensureToggleButton() {
    // KT button intentionally disabled.
    return;
    /*
    if (document.getElementById("keyterms-hover-toggle")) return;
    const paletteForm = document.querySelector("form.md-header__option[data-md-component='palette']");
    if (!paletteForm || !paletteForm.parentElement) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.id = "keyterms-hover-toggle";
    btn.className = "md-header__button keyterms-toggle-button";
    btn.setAttribute("aria-label", "Toggle key term hover definitions");
    btn.addEventListener("click", () => setEnabled(!isEnabled()));
    paletteForm.insertAdjacentElement("afterend", btn);
    setEnabled(isEnabled());
    */
  }

  function init() {
    document.body.setAttribute(BODY_ATTR, isEnabled() ? "1" : "0");
    ensureToggleButton();
    const terms = collectKeyTerms();
    applyInlineTerms(terms);
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(() => init());
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
