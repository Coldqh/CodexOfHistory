/* Codex v1.5 — final startup after every feature module is registered */
(() => {
  syncDiscovery();
  save();
  render();
  window.dispatchEvent(new CustomEvent('codex:ready',{detail:{version:CODEX_MANIFEST.version,cards:CARDS.length}}));
  console.info(`[Codex] v${CODEX_MANIFEST.version}: ${CARDS.length} cards, ${RELATIONS.length} relations, ${CAMPAIGN.nodes.length} missions`);
})();
