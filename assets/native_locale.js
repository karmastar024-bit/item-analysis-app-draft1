(() => {
  // Streamlit/Plotly's built-in controls do not ship a Dzongkha locale.
  // Translate only known control labels, never table cells or uploaded names.
  const lang = __LANGUAGE__;
  const labels = {
    'Save as SVG':'པར་རིས་ཕབ་ལེན།', 'Save as PNG':'པར་རིས་ཕབ་ལེན།',
    'View Source':'བཟོ་ཐབས་བལྟ།', 'View Compiled Vega':'པར་རིས་བཟོ་ཐབས་བལྟ།',
    'Open in Vega Editor':'པར་རིས་ཞུན་དག་ཁ་ཕྱེ།',
    'Deploy':'ཡོངས་འབྲེལ་ཐོག་བཀྲམ།', 'Main menu':'གདམ་ཐོ།',
    'Rerun':'ལོག་ལག་ལེན་འཐབ།', 'Always rerun':'ཨ་རྟག་ར་ལོག་ལག་ལེན་འཐབ།', 'File change.':'ཡིག་སྣོད་སོར་ཡོད།',
    'Scroll tabs right':'གདམ་ཐོ་གཡས་ཁ་ཐུག་སྤོ།', 'Scroll tabs left':'གདམ་ཐོ་གཡོན་ཁ་ཐུག་སྤོ།',
    'XLSX':'ལས་དེབ།', '• XLSX':'• ལས་དེབ།',
    'Upload':'ཡར་བཙུགས་འབད།', 'Browse files':'ཡིག་སྣོད་གདམ་ཁ་རྐྱབས།',
    'Choose File':'ཡིག་སྣོད་གདམ་ཁ་རྐྱབས།', 'Drag and drop file here':'ཡིག་སྣོད་ནཱ་ལུ་འཐེན་བཞག་འབད།',
    'Drag and drop files here':'ཡིག་སྣོད་ཚུ་ནཱ་ལུ་འཐེན་བཞག་འབད།',
    'Fullscreen':'གསལ་གཞི་ཆ་ཚང་།', 'Exit fullscreen':'གསལ་གཞི་ཆ་ཚང་ལས་འཐོན།',
    'Show/hide columns':'ཀེར་ཐིག་སྟོན་ཡང་ན་སྦ་བཞག', 'Download as CSV':'ཐིག་ཁྲམ་ཕབ་ལེན།',
    'Search':'འཚོལ་ཞིབ།', 'Search table':'ཐིག་ཁྲམ་ནང་འཚོལ་ཞིབ།',
    'Download plot as a PNG':'པར་རིས་ཕབ་ལེན།', 'Zoom':'ཆེ་ཆུང་སོར།', 'Pan':'པར་རིས་སྤོ།',
    'Zoom in':'ཆེ་སུ་བཟོ།', 'Zoom out':'ཆུང་སུ་བཟོ།', 'Autoscale':'ཚད་རང་བཞིན་བཟོ།',
    'Reset axes':'ཚད་ཐིག་སྔར་བཞིན་བཟོ།', 'Box Select':'སྒྲོམ་ནང་གདམ་ཁ་རྐྱབས།',
    'Lasso Select':'མཐའ་བསྐོར་ཏེ་གདམ་ཁ་རྐྱབས།', 'Close':'ཁ་བསྡམ།', 'Clear':'བསུབ།',
    'Remove file':'ཡིག་སྣོད་བཏོན་གཏང་།', 'Select all':'ག་ར་གདམ་ཁ་རྐྱབས།',
    'Type to search':'འཚོལ་ཞིབ་དོན་ལུ་བྲིས།', 'No results':'གྲུབ་འབྲས་མེད།'
  };
  const state = window.__resultNativeLocale || { originals: new WeakMap(), attributes: new WeakMap() };
  if (state.observer) state.observer.disconnect();
  const numeral = value => String(value).replace(/[0-9]/g, d => '༠༡༢༣༤༥༦༧༨༩'[Number(d)]);
  function localized(original) {
    if (labels[original]) return labels[original];
    const size = original.match(/^(\d+)\s*MB per file\s*(?:[•·]\s*(?:CSV,?\s*)?XLSX)?$/i);
    if (size) return `ཡིག་སྣོད་རེ་ལུ་ ${numeral(size[1])} མེ་ག་བའིཊ་ཚུན།`;
    return original;
  }
  function text(node) {
    const current = node.nodeValue.trim();
    if (localized(current) !== current) state.originals.set(node, current);
    const original = state.originals.get(node);
    if (!original) return;
    const next = lang === 'dz' ? localized(original) : original;
    if (node.nodeValue !== next) node.nodeValue = next;
  }
  function apply() {
    const scopes = document.querySelectorAll('[data-testid="stFileUploader"], [data-testid="stElementToolbar"], .vega-actions, .modebar, [role="tooltip"], header, button[aria-label="Scroll tabs right"], button[aria-label="Scroll tabs left"]');
    scopes.forEach(scope => {
      [scope, ...scope.querySelectorAll('[aria-label], [title], [data-title], [placeholder]')].forEach(el => {
        const saved = state.attributes.get(el) || {};
        ['aria-label','title','data-title','placeholder'].forEach(attr => {
          const current = el.getAttribute(attr);
          if (current && localized(current) !== current) saved[attr] = current;
          if (!saved[attr]) return;
          const next = lang === 'dz' ? localized(saved[attr]) : saved[attr];
          if (current !== next) el.setAttribute(attr, next);
        });
        state.attributes.set(el, saved);
      });
      const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
      for (let node; (node = walker.nextNode());) text(node);
    });
  }
  let scheduled = false;
  state.observer = new MutationObserver(() => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { scheduled = false; apply(); });
  });
  state.observer.observe(document.body, {childList:true, subtree:true, characterData:true, attributes:true, attributeFilter:['title','data-title','aria-label','placeholder']});
  window.__resultNativeLocale = state;
  apply();
})();
