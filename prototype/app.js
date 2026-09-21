"use strict";
(() => {
  const config = window.RADAR_BALANCE;
  const $ = (id) => document.getElementById(id);
  const labels = ["Billboard edge", "Hedge gap", "Behind the office"];
  const causes = [
    "The billboard hides the housing while leaving most of the measurement corridor open.",
    "This different corridor has slightly more exposure, but a wider measurement window. Knowledge is an editable assumption here.",
    "The building hides the housing and blocks the sensor. Almost invisible does not mean useful: no valid evidence is captured."
  ];
  const positions = [[290, 218, 380, 275], [545, 296, 520, 210], [518, 9, 518, 65]];
  let selected = 0;
  let pinned = null;
  let current;
  const money = (value) => `${Math.round(value).toLocaleString("en-US")} cr`;
  function render() {
    const site = config.sites[selected];
    const e = config.economy;
    const knowledge = Number($("known").value) / 100;
    const flow = Number($("flow").value);
    const clerks = Number($("clerks").value);
    const border = $("border").checked;
    const a = config.awareness;
    const captures = flow * config.traffic.base_speeding * (1 - a.awareness_effect * knowledge)
      * (1 - a.visual_response * site.exposure) * site.coverage * site.quality;
    const domestic = captures * (1 - config.traffic.foreign_share);
    const foreign = border ? captures * config.traffic.foreign_share : 0;
    const capacity = e.base_capacity + clerks * e.clerk_capacity + (border ? e.border_capacity : 0);
    const work = domestic + 2 * foreign;
    const fraction = work > 0 ? Math.min(1, capacity / work) : 0;
    const receipts = fraction * (domestic * e.domestic_payment_probability + foreign * e.foreign_payment_probability) * e.experiment_fine;
    const costs = e.fixed_upkeep + clerks * e.clerk_wage + (border ? e.border_wage : 0);
    const net = receipts - costs;
    $("known-label").textContent = `${Math.round(knowledge * 100)}%`;
    $("flow-label").textContent = flow;
    $("panel-title").textContent = labels[selected];
    $("cause").textContent = causes[selected];
    for (const key of ["exposure", "coverage", "quality"]) {
      $(key).value = site[key];
      $(`${key}-value`).textContent = `${Math.round(site[key] * 100)}%`;
    }
    $("net").textContent = `${money(net)} / shift`;
    $("case-estimate").textContent = `${captures.toFixed(1)} estimated cases · ${(fraction * (domestic + foreign)).toFixed(1)} processed`;
    $("bottleneck").textContent = site.coverage === 0 ? "No sensor path. Staff and device costs continue." :
      work > capacity ? "Office overloaded. Photos can outpace processing capacity." :
      !border ? "Foreign cases remain ineligible without a specialist." : "Office capacity can handle this estimated flow.";
    $("purchase").textContent = money(e.fixed_purchase);
    $("cost").textContent = money(costs);
    $("capacity").textContent = `${capacity} work units`;
    const [x, y, tx, ty] = positions[selected];
    $("sensor-dot").setAttribute("cx", x);
    $("sensor-dot").setAttribute("cy", y);
    $("sensor-ray").setAttribute("d", `M${x} ${y} L${tx} ${ty}`);
    document.querySelectorAll("[data-site]").forEach((button) => button.setAttribute("aria-pressed", String(Number(button.dataset.site) === selected)));
    current = {name: labels[selected], net, knowledge: Math.round(knowledge * 100), flow, clerks, border};
    $("comparison").textContent = pinned ?
      `${pinned.name}: ${money(pinned.net)}/shift at ${pinned.flow} cars/shift, ${pinned.knowledge}% knowledge, ${pinned.clerks} clerk(s), ${pinned.border ? "with" : "without"} border specialist. Current forecast: ${money(net - pinned.net)}/shift difference.` :
      "Pin a scenario, then change the site, driver knowledge, or office capacity.";
  }
  document.querySelectorAll("[data-site]").forEach((button) => button.addEventListener("click", () => {
    selected = Number(button.dataset.site); render();
  }));
  ["known", "flow", "clerks", "border"].forEach((id) => $(id).addEventListener("input", render));
  $("pin").addEventListener("click", () => {pinned = {...current}; render();});
  $("reset").addEventListener("click", () => {
    selected = 0; pinned = null; $("known").value = 20; $("flow").value = config.traffic.flow_per_shift;
    $("clerks").value = 1; $("border").checked = false; render();
  });
  $("flow").value = config.traffic.flow_per_shift;
  render();
})();
