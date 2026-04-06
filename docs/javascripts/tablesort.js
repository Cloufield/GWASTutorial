(function () {
  function initTableSort() {
    if (typeof Tablesort === "undefined") return;
    document.querySelectorAll("article table:not([class])").forEach(function (table) {
      if (table.dataset.gwtTablesortInit === "1") return;
      if (!table.tHead || table.tHead.rows.length === 0) return;
      table.dataset.gwtTablesortInit = "1";
      new Tablesort(table);
    });
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(initTableSort);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTableSort);
  } else {
    initTableSort();
  }
})();
