#prompt_builder.py

from coaching_profile import REPORT_CONTRACT, REPORT_RESOLUTION, RENDERER_PROFILES
from textwrap import dedent

def build_system_prompt_from_header(report_type: str, header: dict) -> str:
    """
    Build deterministic renderer instructions for GPT based on the
    URF v5.1 report contract.

    This output is DATA ONLY and must be used as a system-role message
    by the caller.
    """
    from coaching_profile import RENDERER_PROFILES
    from textwrap import dedent

    title = header.get("title", f"{report_type.title()} Report")
    scope = header.get("scope", "Training and wellness summary")
    sources = header.get("data_sources", "Intervals.icu activity and wellness datasets")
    intended = header.get("intended_use", "General endurance coaching insight")
    contract_sections = REPORT_CONTRACT.get(report_type, [])
    contract_version = "URF v5.1"

    # --------------------------------------------------
    # Resolve section order from contract
    # --------------------------------------------------
    if isinstance(contract_sections, dict):
        section_order = list(contract_sections.keys())
    else:
        section_order = contract_sections or ["Summary", "Metrics", "Actions"]

    manifest_lines = [f"{i}. {section}" for i, section in enumerate(section_order, start=1)]

    # --------------------------------------------------
    # Resolve renderer profiles
    # --------------------------------------------------
    global_profile = RENDERER_PROFILES.get("global", {})
    report_profile = RENDERER_PROFILES.get(report_type, {})

    stack_structure = report_profile.get("stack_structure", {})

    hard_rules = global_profile.get("hard_rules", [])
    list_rules = global_profile.get("list_rules", [])
    tone_rules = global_profile.get("tone_rules", [])

    interpretation_rules = report_profile.get("interpretation_rules", [])
    allowed_enrichment = report_profile.get("allowed_enrichment", [])

    coaching_cfg = report_profile.get("coaching_sentences", {})
    coaching_enabled = coaching_cfg.get("enabled", False)
    coaching_max = coaching_cfg.get("max_per_section", 0)

    section_handling = report_profile.get("section_handling", {})
    stack_labels = report_profile.get("stack_labels", {})
    signal_hierarchy = report_profile.get("signal_hierarchy", [])
    fatigue_logic = report_profile.get("fatigue_logic", [])
    question_themes = report_profile.get("question_rule", [])
    events_rule = report_profile.get("events_rule")
    planned_events_rule = report_profile.get("planned_events_rule")
    resolution = REPORT_RESOLUTION.get(report_type, {})

    # ➕ NEW: presentation config (read directly, no helpers)
    state_presentation = global_profile.get("state_presentation", {})
    emphasis = report_profile.get("emphasis", {})
    framing = report_profile.get("framing", {})
    closing_cfg = report_profile.get("closing_note", {})
    post_render = report_profile.get("post_render", {})

    # --------------------------------------------------
    # Optional blocks (existing)
    # --------------------------------------------------

    stack_map_lines = []

    for layer, sections in stack_structure.items():
        label = stack_labels.get(layer, layer.upper())

        for section in sections:
            stack_map_lines.append(f"{section} → {label}")
    #-----------------------------------------------------------------
    stack_lines = []
    for layer, sections in stack_structure.items():
        label = stack_labels.get(layer, layer.upper())

        stack_lines.append(label)
        for s in sections:
            stack_lines.append(f"- {s}")
    #-----------------------------------------------------------------
    stack_block = ""
    if stack_structure:

        stack_lines = []

        for layer, sections in stack_structure.items():

            layer_name = layer.replace("_", " ").title()

            stack_lines.append(f"{layer_name}:")
            for s in sections:
                stack_lines.append(f"- {s}")

            stack_lines.append("")

        stack_block = dedent(f"""
        STACK STRUCTURE RULE:

        The report MUST be organised into the following conceptual intelligence layers:

        {chr(10).join(stack_lines)}

        These layers are PRESENTATIONAL GROUPINGS ONLY.

        They must NOT:
        - change section order
        - override section_handling rules
        - modify interpretation_rules
        - alter table rendering rules

        Sections must appear in the exact URF contract order.
        Stack layers only determine which layer header a section appears under.

        Each section must appear under its corresponding stack layer while still following the URF section order.
        A stack layer header MUST be rendered once when the first section belonging to that layer appears.
        Subsequent sections mapped to the same stack layer MUST remain under that header and MUST NOT repeat the header.
        """).strip()
    #-----------------------------------------------------------------
    stack_map_block = ""

    if stack_map_lines:
        stack_map_block = dedent(f"""
        STACK SECTION MAP:
        {chr(10).join(stack_map_lines)}
        """).strip()

    resolution_block = ""
    #-----------------------------------------------------------------
    if resolution:
        resolution_block = dedent(f"""
        DATA RESOLUTION MODEL:

        This report uses the following semantic resolution rules.

        {chr(10).join(f"- {k}: {v}" for k, v in resolution.items())}

        These rules determine which metrics are authoritative,
        which signals may appear, and the time horizon used
        for interpretation.

        Resolution rules MUST NOT be printed in the report output.
        """).strip()
    #-----------------------------------------------------------------
    section_handling_block = ""
    if section_handling:
        section_handling_block = dedent(f"""
        SECTION HANDLING RULES:
        {chr(10).join(f"- {k}: {v}" for k, v in section_handling.items())}

        Handling meanings:

        - full:
            Render the entire section exactly as provided.
            Tables remain tables, lists remain lists.
            Do not remove rows or fields.

        - summary:
            Render a compact representation using ONLY existing semantic aggregates
            already present in the section. Do NOT derive new metrics.

        Summary rules:
            Prefer a short table if aggregate values exist.
            If aggregates do not exist, show the top-level fields only.
            Do NOT iterate full arrays or lists.
            Do NOT narrate each element of a list.
            Maximum 3–5 rows or key metrics.

        - table_summary:
            Render a condensed table using aggregate fields only.
            Do NOT render the full underlying dataset.

        - headline:
            Render only the primary indicators of the section.
            Maximum 3–4 metrics.
            No tables longer than one row.
            No subsections.
            No detailed narrative.

        Rules:
        • Maximum 5 rows.
        • Prefer totals, means, or trend indicators already provided.
        • Do NOT derive calculations.

        - forbid:
        This section MUST NOT be rendered in the report output.
        It may still be used internally for reasoning.
        """).strip()
    #-----------------------------------------------------------------
    closing_note_block = ""

    if closing_cfg.get("required"):
        verdict_rule = closing_cfg.get("verdict_rule", "")
        classifications = closing_cfg.get("classification_required", [])
        focus = closing_cfg.get("focus", "")
        intent = closing_cfg.get("intent_rule", "")
        anchors = closing_cfg.get("anchor_metrics", [])
        exact_sent = closing_cfg.get("exact_sentences")
        max_sent = closing_cfg.get("max_sentences")
        sentence_structure = closing_cfg.get("sentence_structure", [])

        closing_note_block = dedent(f"""
        CLOSING NOTE REQUIREMENTS:
        - The closing note MUST begin with one of the following classifications:
        {", ".join(classifications)}.
        - {verdict_rule}
        - The closing note MUST remain within the conceptual focus: {focus}.
        - {intent}
        - It MUST anchor strictly to: {", ".join(anchors)}.
        - It MUST NOT introduce new metrics or reinterpret semantic data.
        """).strip()

        if exact_sent:
            closing_note_block += f"\n- The closing note MUST contain exactly {exact_sent} sentences."
        elif max_sent:
            closing_note_block += f"\n- Maximum {max_sent} sentences."

        if sentence_structure:
            closing_note_block += "\n- The six sentences MUST follow this structure:"
            for s in sentence_structure:
                closing_note_block += f"\n  {s}"
    #-----------------------------------------------------------------
    post_render_block = ""

    post_cfg = report_profile.get("post_render", {}).get("explore_deeper", {})

    if post_cfg.get("enabled"):
        commands = post_cfg.get("commands", [])

        post_render_block = dedent(f"""
        POST-RENDER INTERACTION:
        - After the full report is rendered, present follow-up commands to allow deeper inspection.
        - These commands MUST be shown after the closing reflection section.
        - The commands MUST be rendered as short, copyable user prompts in raw markdown
        - Do NOT add explanation, narrative, or coaching around these commands.

        Suggested follow up questions:
        {chr(10).join([f'- "{cmd}"' for cmd in commands])}
        """).strip()
    #-----------------------------------------------------------------
    coaching_block = ""
    if coaching_enabled and coaching_max > 0:
        coaching_block = dedent(f"""
        COACHING INTERPRETATION RULES:
        - You are an Endurance Coach
        - You MAY include up to {coaching_max} short coaching sentence(s) per section.
        - Coaching sentences MUST be directly anchored to values, states, or interpretation fields in that section.
        - Coaching sentences MUST be descriptive or conditional, not predictive.
        - Coaching sentences MUST appear immediately after the section’s data and before the next divider.
        - Coaching sentences MUST NOT introduce new metrics.
        """).strip()

    #-----------------------------------------------------------------
    question_block = ""
    if coaching_enabled and question_themes:
        question_block = dedent(f"""
        CLOSING REFLECTION RULE:
        After the full report is produced, generate exactly ONE short reflective coaching question.

        The question MUST be based on the dominant signal in the report.

        Allowed reflection themes:
        {chr(10).join(f"- {t}" for t in question_themes)}

        The closing question must be grounded in the signals present in the report
        and must not introduce new metrics or predictions.

        Format exactly as:
        ---
        Closing Reflection
        <question>
        """).strip()
    #-----------------------------------------------------------------
    enrichment_block = ""
    if allowed_enrichment:
        enrichment_block = dedent(f"""
        ALLOWED ENRICHMENT:
        {chr(10).join(f"- {r}" for r in allowed_enrichment)}
        """).strip()
    #-----------------------------------------------------------------
    events_block = ""

    if events_rule:
        icon_list = "\n".join(
            f"{i+1}) {icon}" for i, icon in enumerate(events_rule.get("icons", []))
        )

        duration_rules = "\n".join(f"- {r}" for r in events_rule.get("duration_conversion", []))
        rules = "\n".join(f"- {r}" for r in events_rule.get("rules", []))

        columns = " | ".join(events_rule.get("column_order", []))

        events_block = dedent(f"""
        EVENTS (WEEKLY — NON-NEGOTIABLE):
        {rules}

        - The EVENTS table MUST use the following column order:
        {columns}

        {duration_rules}

        - When multiple icons apply, they MUST be rendered together in the following fixed order (left → right):
        {icon_list}
        """).strip()
    #-----------------------------------------------------------------
    planned_events_block = ""

    if planned_events_rule:
        planned_events_block = dedent(f"""
        PLANNED EVENTS (WEEKLY — NON-NEGOTIABLE):
        {chr(10).join(f"- {r}" for r in planned_events_rule)}
        """).strip()

    # --------------------------------------------------
    state_presentation_block = ""
    if state_presentation.get("enabled"):
        state_presentation_block = dedent(f"""
        STATE PRESENTATION:
        - Present a concise, single-sentence state banner at the top of the report.
        - Use ONLY semantic states already present in the data.
        - Do NOT derive, compute, or infer new states.
        - Style: {state_presentation.get("style")}
        """).strip()
    #-----------------------------------------------------------------
    emphasis_block = ""
    if emphasis:
        emphasis_block = dedent(f"""
        EMPHASIS GUIDANCE:
        The following sections should receive proportional narrative and visual emphasis.
        This does NOT change section order, inclusion, or data fidelity.
        {chr(10).join(f"- {k}: {v}" for k, v in emphasis.items())}
        """).strip()
    #-----------------------------------------------------------------
    framing_block = ""
    if framing:
        framing_block = dedent(f"""
        FRAMING INTENT:
        - Interpret and summarise this report through the following intent:
          {framing.get("intent")}
        - This intent guides prioritisation and narrative focus only.        
        """).strip()
    # --------------------------------------------------
    # Welness blocks
    # --------------------------------------------------
    fatigue_block = ""
    if fatigue_logic:
        fatigue_block = dedent(f"""
        FATIGUE INTERPRETATION MODEL:
        {chr(10).join(f"- {r}" for r in fatigue_logic)}
        """).strip()
    #-----------------------------------------------------------------
    signal_block = ""
    if signal_hierarchy:
        signal_block = dedent(f"""
        SIGNAL PRIORITY MODEL:
        Interpret recovery signals using the following hierarchy.
        Earlier layers take precedence when signals disagree.

        {chr(10).join(f"- {s}" for s in signal_hierarchy)}
        """).strip()
    # --------------------------------------------------
    # Assemble final prompt
    # --------------------------------------------------
    prompt = dedent(f"""
    You are a deterministic URF renderer.

    You must render a **{title}** using the embedded system context.
    This report follows the **Unified Reporting Framework ({contract_version})**.

    **Scope:** {scope}
    **Data Sources:** {sources}
    **Intended Use:** {intended}
    {resolution_block}
    HARD RULES:
    {chr(10).join(f"- {r}" for r in hard_rules)}

    {stack_block}

    {stack_map_block}

    INTERPRETATION RULES:
    {chr(10).join(f"- {r}" for r in interpretation_rules)}

    {coaching_block}

    {enrichment_block}

    {signal_block}

    {fatigue_block}

    {state_presentation_block}

    {emphasis_block}

    {framing_block}

    {section_handling_block}

    {events_block}

    {planned_events_block}

    LIST RENDERING RULES (NON-NEGOTIABLE):
    {chr(10).join(f"- {r}" for r in list_rules)}

    TONE AND STYLE:
    {chr(10).join(f"- {r}" for r in tone_rules)}

    SECTION ORDER (INSTRUCTIONAL — DO NOT NUMBER HEADERS):
    {chr(10).join(manifest_lines)}

    {closing_note_block}

    {question_block}

    {post_render_block}
    
    """).strip()

    return prompt





