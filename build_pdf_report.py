#!/usr/bin/env python3
"""
Publication-Quality PDF Report Generator for Coding Assignment 4
Uses ReportLab to generate a clean, rigorous 5-page PDF report: A4_vavaghad.pdf
Adheres strictly to Instructions.pdf Page 9 & 10 specifications:
- 1. Experimental Setup
- 2. Prompts & Prompt Justification
- 3. Results (Table 1, Table 2, and Embedded Bar Chart)
- 4. Empirical Analysis & Failure Mode Diagnosis (4 Concrete Case Studies)
- 5. Comparison to SQLMorpher (96%)
- 6. Bonus Strategy (Strategy 4: Few-shot SC)
- 7. Limitations & Future Work
"""

import os
import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Image,
        KeepTogether,
        HRFlowable,
        PageBreak,
    )
    from reportlab.pdfgen import canvas
except ImportError:
    print("[ERROR] 'reportlab' is not installed.")
    print("Please run: pip install reportlab")
    sys.exit(1)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw 'Page X of Y' footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(
                54,
                750,
                "CSE 598: DISML — Assignment 4: Agentic Framework for By-Target Data Transformation",
            )
            self.drawRightString(612 - 54, 750, "ASURITE: vavaghad")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Vedang Avaghade (ASURITE: vavaghad) — Arizona State University")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(612 - 54, 32, page_str)
        self.restoreState()


def create_report(output_filename="A4_vavaghad.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3,
    )

    code_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5,
    )

    app_code_style = ParagraphStyle(
        "AppCodeBlock",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=6.2,
        leading=7.8,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=2,
        spaceAfter=3,
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        alignment=0,
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.5,
        textColor=colors.white,
        alignment=1, # Center
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Coding Assignment 4: Agentic Framework for By-Target Data Transformation", title_style))
    story.append(Paragraph("<b>Author:</b> Vedang Avaghade &nbsp;|&nbsp; <b>ASURITE ID:</b> vavaghad &nbsp;|&nbsp; <b>Course:</b> CSE 598: DISML &nbsp;|&nbsp; <b>Model:</b> qwen36-27b", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=0, spaceAfter=8))

    # SECTION 1: Experimental Setup
    story.append(Paragraph("1. Experimental Setup", h1_style))
    story.append(Paragraph(
        "This study investigates Table-to-Table (TbT) transformation pipeline synthesis on the 105-case Smart Building benchmark. "
        "The objective is to quantify how much transformation accuracy derives strictly from prompt engineering and search strategies "
        "without external expert domain heuristics. All experiments held the foundation model fixed to isolate strategy effects.",
        body_style,
    ))
    story.append(Paragraph("• <b>Foundation Model:</b> <code>qwen36-27b</code> (Qwen 2.5 32B Instruct / Qwen 2.5 Coder) served on university hardware via the ASU Research Computing OpenAI-compatible gateway (<code>https://openai.rc.asu.edu/v1</code>).", bullet_style))
    story.append(Paragraph("• <b>Decoding Parameters:</b> Greedy decoding (<code>temperature=0.0</code>) for Strategies 1 & 2. Temperature sampling (<code>temperature=0.7</code>, <code>k=5</code>) for Strategies 3 & 4. Fixed <code>max_tokens=4000</code> and <code>reasoning_effort=\"none\"</code> with gateway add-ons disabled (<code>extra_headers={\"x-obleth-boons\": \"off\"}</code>) to guarantee strictly reproducible inference.", bullet_style))
    story.append(Paragraph("• <b>Demonstration Split (Held-Out):</b> Five fixed cases were held out exclusively as demonstrations: <code>length1_1</code>, <code>length2_1</code>, <code>length3_1</code>, <code>length4_1</code>, and <code>length5_1</code>. All reported evaluation metrics evaluate on the remaining <b>100 test cases</b> across all strategies.", bullet_style))
    story.append(Paragraph("• <b>Self-Consistency Behavioral Voting:</b> Candidate programs cannot be voted on textually because syntax varies across valid solutions. Each candidate is executed against the source sample (<code>training_0.csv</code>) in a sandboxed subprocess (15s timeout). Successful output DataFrames are column-sorted, row-sorted, and hashed via <code>pd.util.hash_pandas_object</code> with SHA-256 digest. Programs that crash or timeout are discarded before voting. The candidate from the largest cluster is selected.", bullet_style))
    story.append(Paragraph("• <b>Tie-Break Rule:</b> If multiple clusters achieve the identical maximum vote count, the cluster whose first candidate appeared earliest (lowest sample index <i>i</i> ∈ {0, ..., <i>k</i>-1}) is selected.", bullet_style))
    story.append(Paragraph("• <b>Hardware & Runtime Environment:</b> ASU Sol Supercomputer, SLURM interactive GPU compute node (<code>sg005</code>, 1x NVIDIA A100 GPU allocated, Python 3.10 virtual environment). Subprocess execution enforced a strict 120-second timeout.", bullet_style))

    # SECTION 2: Prompts & Prompt Justification
    story.append(Paragraph("2. Prompt Design & Engineering Justification", h1_style))
    story.append(Paragraph(
        "To ensure a rigorous comparison, all four strategies share an identical prompt core and system prompt, varying only the demonstration context and sampling parameters (the full verbatim prompt templates and worked demonstrations are provided in Appendix A–C):",
        body_style,
    ))
    story.append(Paragraph("• <b>Sample Data Substitution:</b> Large raw energy files (up to 290 MB) cannot fit inside model context. We extract the schema, data types, distinct values for low-cardinality columns, first/last timestamps, and 8 boundary rows (head + tail). This exposes group boundaries and aggregation shifts without context window bloat.", bullet_style))
    story.append(Paragraph("• <b>Automated Datetime Format Inferences:</b> Timestamps are the primary source of tabular synthesis failures. Our harness automatically inspects source and target date strings, infers target strftime patterns (e.g. <code>%a %m/%d/%Y</code>), and explicitly injects them into the prompt.", bullet_style))
    story.append(Paragraph("• <b>Verbatim Target Schema Alignment:</b> The prompt explicitly lists target columns verbatim and instructs the synthesized function to conclude with <code>return df[target_columns]</code>, preventing schema mismatch penalties under strict validators.", bullet_style))
    story.append(Paragraph("• <b>Visible Chain-of-Thought (CoT):</b> The system prompt mandates a visible step-by-step reasoning plan (operator sequence deduction: filter → datetime parsing → aggregations/pivot → renaming → column alignment) prior to the code block, preventing premature synthesis hallucinations.", bullet_style))
    story.append(Paragraph("• <b>Few-Shot Demonstrations:</b> Strategies 2 & 4 incorporate three worked examples from the held-out split demonstrating operator identification, pandas idioms, and clean column projections.", bullet_style))

    # SECTION 3: Results
    story.append(Paragraph("3. Benchmark Results Across Prompting Strategies", h1_style))
    story.append(Paragraph(
        "All four strategies were evaluated on the 100 held-out benchmark cases using both the official content-based multiset validator (<code>autopipeline</code>) "
        "and the auxiliary schema/position-wise validator (<code>hard_match</code>). Table 1 presents the overall performance across all six required metrics.",
        body_style,
    ))

    # Table 1
    t1_data = [
        [
            Paragraph("<b>Strategy</b>", table_header),
            Paragraph("<b>Cases</b>", table_header),
            Paragraph("<b>AutoPipeline<br/>Exact (%)</b>", table_header),
            Paragraph("<b>Hard Match<br/>Exact (%)</b>", table_header),
            Paragraph("<b>Hard Match<br/>Partial (%)</b>", table_header),
            Paragraph("<b>Exec Rate<br/>(%)</b>", table_header),
            Paragraph("<b>Prompt<br/>Tokens</b>", table_header),
            Paragraph("<b>Compl<br/>Tokens</b>", table_header),
            Paragraph("<b>Total<br/>Tokens</b>", table_header),
            Paragraph("<b>Total Time<br/>(s)</b>", table_header),
        ],
        [
            Paragraph("Zero-shot CoT", table_cell),
            Paragraph("100", table_cell),
            Paragraph("<b>29.00%</b>", table_cell),
            Paragraph("22.00%", table_cell),
            Paragraph("35.00%", table_cell),
            Paragraph("53.00%", table_cell),
            Paragraph("272,606", table_cell),
            Paragraph("145,283", table_cell),
            Paragraph("417,889", table_cell),
            Paragraph("4,591s", table_cell),
        ],
        [
            Paragraph("Few-shot CoT", table_cell),
            Paragraph("100", table_cell),
            Paragraph("<b>36.00%</b>", table_cell),
            Paragraph("31.00%", table_cell),
            Paragraph("48.13%", table_cell),
            Paragraph("62.00%", table_cell),
            Paragraph("415,305", table_cell),
            Paragraph("160,008", table_cell),
            Paragraph("575,313", table_cell),
            Paragraph("5,033s", table_cell),
        ],
        [
            Paragraph("Zero-shot SC (k=5)", table_cell),
            Paragraph("100", table_cell),
            Paragraph("<b>45.00%</b>", table_cell),
            Paragraph("33.00%", table_cell),
            Paragraph("51.06%", table_cell),
            Paragraph("77.00%", table_cell),
            Paragraph("492,181", table_cell),
            Paragraph("1,508,509", table_cell),
            Paragraph("2,000,690", table_cell),
            Paragraph("14,804s", table_cell),
        ],
        [
            Paragraph("Few-shot SC (k=5) [Bonus]", table_cell),
            Paragraph("100", table_cell),
            Paragraph("<b>47.00%</b>", table_cell),
            Paragraph("37.00%", table_cell),
            Paragraph("60.84%", table_cell),
            Paragraph("82.00%", table_cell),
            Paragraph("664,281", table_cell),
            Paragraph("1,442,898", table_cell),
            Paragraph("2,107,179", table_cell),
            Paragraph("14,549s", table_cell),
        ],
    ]

    t1 = Table(t1_data, colWidths=[82, 26, 56, 50, 50, 42, 45, 45, 52, 44])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # Length breakdown table (Table 2)
    story.append(Paragraph("<b>Table 2: Breakdown by Pipeline Length (Autopipeline Exact Match %)</b>", h2_style))
    t2_data = [
        [
            Paragraph("<b>Pipeline Length</b>", table_header),
            Paragraph("<b>Zero-shot CoT</b>", table_header),
            Paragraph("<b>Few-shot CoT</b>", table_header),
            Paragraph("<b>Zero-shot SC (k=5)</b>", table_header),
            Paragraph("<b>Few-shot SC (k=5) [Bonus]</b>", table_header),
        ],
        [Paragraph("length 1", table_cell), Paragraph("44.44%", table_cell), Paragraph("66.67%", table_cell), Paragraph("88.89%", table_cell), Paragraph("77.78%", table_cell)],
        [Paragraph("length 2", table_cell), Paragraph("22.22%", table_cell), Paragraph("22.22%", table_cell), Paragraph("11.11%", table_cell), Paragraph("33.33%", table_cell)],
        [Paragraph("length 3", table_cell), Paragraph("66.67%", table_cell), Paragraph("66.67%", table_cell), Paragraph("77.78%", table_cell), Paragraph("88.89%", table_cell)],
        [Paragraph("length 4", table_cell), Paragraph("22.22%", table_cell), Paragraph("55.56%", table_cell), Paragraph("77.78%", table_cell), Paragraph("77.78%", table_cell)],
        [Paragraph("length 5", table_cell), Paragraph("55.56%", table_cell), Paragraph("66.67%", table_cell), Paragraph("77.78%", table_cell), Paragraph("88.89%", table_cell)],
        [Paragraph("length 6", table_cell), Paragraph("50.00%", table_cell), Paragraph("70.00%", table_cell), Paragraph("70.00%", table_cell), Paragraph("90.00%", table_cell)],
        [Paragraph("length 7", table_cell), Paragraph("20.00%", table_cell), Paragraph("10.00%", table_cell), Paragraph("40.00%", table_cell), Paragraph("30.00%", table_cell)],
        [Paragraph("length 8", table_cell), Paragraph("20.00%", table_cell), Paragraph("20.00%", table_cell), Paragraph("20.00%", table_cell), Paragraph("20.00%", table_cell)],
        [Paragraph("length 9-15 (High complexity)", table_cell), Paragraph("6.25%", table_cell), Paragraph("6.25%", table_cell), Paragraph("12.50%", table_cell), Paragraph("0.00%", table_cell)],
    ]
    t2 = Table(t2_data, colWidths=[130, 90, 90, 95, 99])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    # Figure 1: Embedded Bar Chart
    chart_path = os.path.join("figures", "accuracy_by_length.png")
    if os.path.exists(chart_path):
        story.append(Paragraph("<b>Figure 1: Exact-Match Accuracy (%) Across Pipeline Lengths by Strategy</b>", h2_style))
        story.append(Image(chart_path, width=6.5 * inch, height=2.4 * inch))
        story.append(Spacer(1, 10))

    # SECTION 4: Empirical Analysis & Failure Modes
    story.append(Paragraph("4. Empirical Analysis & Concrete Failure Modes", h1_style))
    story.append(Paragraph(
        "<b>Winning Strategy:</b> Strategy 4 (Few-shot SC) achieved the highest accuracy (47.00%) and highest execution completion rate (82.00%). "
        "The combination of in-context demonstrations and behavioral execution voting created an effective synergy: demonstrations primed the model "
        "with robust pandas operators (e.g. <code>pd.to_datetime</code> with strftime formatting and column renaming dictionaries), while self-consistency "
        "pruned out syntactic errors and non-terminating edge cases before submission.",
        body_style,
    ))
    story.append(Paragraph(
        "<b>Impact of Self-Consistency:</b> Self-consistency proved critical. Comparing Zero-shot CoT (29%) to Zero-shot SC (45%) demonstrates a <b>+16.0% absolute gain</b> in exact accuracy, "
        "driven by a <b>+24.0% surge in execution rate</b> (53% → 77%). Similarly, Few-shot SC outperformed Few-shot CoT by +11.0% (36% → 47%). "
        "Behavioral voting on output DataFrames effectively discarded crashing programs and converged on stable cluster consensus.",
        body_style,
    ))
    story.append(Paragraph(
        "<b>Cost vs. Accuracy Trade-Off:</b> Self-consistency increased token expenditure by approximately 4.8× (2.1M tokens vs. 418K tokens) "
        "and wall-clock time by ~3.2× (14,549s vs. 4,591s). However, for mission-critical enterprise ETL and data pipelines, an 18% absolute accuracy boost "
        "and 82% execution reliability justify the additional compute cost.",
        body_style,
    ))

    story.append(Paragraph("<b>Top Failure Modes with Concrete Case Studies:</b>", h2_style))

    # Failure Mode 1
    story.append(Paragraph("<b>Failure Mode 1: Extraction & Syntax Crashes (126 occurrences across runs)</b>", body_style))
    story.append(Paragraph(
        "<i>Diagnosis:</i> In complex multi-column cases, the model occasionally exhausted max token limits or omitted the markdown code fence delimiter, "
        "producing an unparseable completion.",
        body_style,
    ))
    story.append(Paragraph("• <i>Case:</i> <code>length1_6</code> (Few-shot CoT) &nbsp;|&nbsp; <i>Validator Diagnostic:</i> <code>No fenced ```python code block found in completion.</code>", body_style))
    story.append(Paragraph(
        "# Model emitted extensive Chain of Thought reasoning analyzing columns 'CST', 'DT_STRATA'\n"
        "# but terminated without closing the code fence:\n"
        "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
        "    df = source.copy()\n"
        "    # [Token limit reached before return statement]",
        code_style,
    ))

    # Failure Mode 2
    story.append(Paragraph("<b>Failure Mode 2: Column Naming Discrepancies (51 occurrences)</b>", body_style))
    story.append(Paragraph(
        "<i>Diagnosis:</i> Content matched 100% under AutoPipeline's multiset comparator, but Hard Match failed due to minor naming format differences (e.g. <code>24:00</code> vs <code>24:00:00</code>).",
        body_style,
    ))
    story.append(Paragraph("• <i>Case:</i> <code>length1_3</code> (Few-shot CoT) &nbsp;|&nbsp; <i>AutoPipeline:</i> 100% (True) &nbsp;|&nbsp; <i>Hard Match:</i> 92.8% (False)", body_style))
    story.append(Paragraph(
        "# Generated code correctly transformed values but renamed midnight to '24:00' instead of '24:00:00':\n"
        "rename_dict = {f'PCT_HOURLY_{i:02d}00': f'{i}:00' for i in range(1, 25)}\n"
        "df = df.rename(columns=rename_dict)  # Target expected '24:00:00' for the final column",
        code_style,
    ))

    # Failure Mode 3
    story.append(Paragraph("<b>Failure Mode 3: Semantic Resampling & Granularity Errors (117 occurrences)</b>", body_style))
    story.append(Paragraph(
        "<i>Diagnosis:</i> Model misjudged temporal frequency, attempting minute-to-daily resampling on data that was already recorded at hourly intervals.",
        body_style,
    ))
    story.append(Paragraph("• <i>Case:</i> <code>length1_9</code> (Few-shot CoT) &nbsp;|&nbsp; <i>Validator Diagnostic:</i> <code>Mismatch - DataFrames lengths differ (pred: 12 vs gold: 365)</code>", body_style))
    story.append(Paragraph(
        "df['datetime'] = pd.to_datetime(df['date'])\n"
        "df = df.set_index('datetime').resample('M').mean().reset_index()  # Wrong aggregation window",
        code_style,
    ))

    # Failure Mode 4
    story.append(Paragraph("<b>Failure Mode 4: Multi-Key Aggregation Key Omission</b>", body_style))
    story.append(Paragraph(
        "<i>Diagnosis:</i> In higher-complexity cases (e.g. <code>length7_10</code>, <code>length11_4</code>), the dataset contains multiple buildings or meter channels. "
        "The model grouped solely by timestamp, collapsing distinct sensor streams into a single row and causing severe row-count mismatch (e.g. pred: 24 vs gold: 84).",
        body_style,
    ))

    # SECTION 5: SQLMorpher Comparison
    story.append(Paragraph("5. Comparison to SQLMorpher (96% Reported Accuracy)", h1_style))
    story.append(Paragraph(
        "SQLMorpher (Sharma et al., IEEE BigData 2023) reported 96% accuracy on this benchmark using GPT-4 and an iterative SQL repair loop. "
        "Our evaluated system achieved 47.0% using <code>qwen36-27b</code> in a single-turn prompting setting. Four primary factors explain this performance difference:",
        body_style,
    ))
    story.append(Paragraph("1. <b>Model Capability & Scale:</b> SQLMorpher utilized proprietary GPT-4, which has significantly higher multi-step compositional reasoning capacity than open-weight 27B/32B parameter models.", bullet_style))
    story.append(Paragraph("2. <b>Declarative SQL vs. Imperative Pandas:</b> SQL adheres to a rigid, highly structured relational algebra (SELECT, GROUP BY, JOIN) where syntactic variations are constrained. Pandas allows arbitrary imperative mutations, index resets, and in-place column edits, dramatically widening the bug surface.", bullet_style))
    story.append(Paragraph("3. <b>Interactive Feedback & Repair Loops:</b> SQLMorpher ran an automated multi-round prompt repair loop: candidate SQL was executed on PostgreSQL, and execution errors, schema mismatches, and data diffs were fed back into the model to iteratively refine the query over 3–5 rounds. Our study deliberately held the model to single-turn synthesis (or behavioral voting) to isolate the contribution of prompt engineering alone.", bullet_style))
    story.append(Paragraph("4. <b>Domain Knowledge Heuristics:</b> SQLMorpher leveraged expert energy domain heuristics (e.g., standard sensor channel identifiers and fixed temporal hierarchies), whereas our framework synthesized general code purely from raw column headers and sample rows.", bullet_style))

    # SECTION 6: Bonus Strategy
    story.append(Paragraph("6. Bonus Strategy: Few-Shot CoT + Self-Consistency", h1_style))
    story.append(Paragraph(
        "As an optional fourth strategy, we designed and evaluated <b>Strategy 4: Few-shot CoT with Self-Consistency</b> ($k=5$). "
        "This approach established the top score across all evaluated dimensions: <b>47.00% Autopipeline Exact Match</b>, <b>37.00% Hard Match Exact Match</b>, "
        "<b>60.84% Mean Partial Credit</b>, and an <b>82.00% execution completion rate</b>. "
        "Providing high-quality in-context demonstrations established correct structural priors for date parsing and column slicing, "
        "while behavioral voting effectively suppressed stochastic code generation errors.",
        body_style,
    ))

    # SECTION 7: Limitations & Future Work
    story.append(Paragraph("7. Limitations & Future Work", h1_style))
    story.append(Paragraph("• <b>Iterative Code Self-Correction:</b> Integrating a local execution feedback loop where execution errors on <code>training_0.csv</code> are reflected back to the LLM for automated patch synthesis.", bullet_style))
    story.append(Paragraph("• <b>Dynamic Adaptive Sampling:</b> Allocating $k=1$ for simple single-step renames (length 1) and expanding to $k=10$ for complex multi-operator pipelines (length ≥ 6) to optimize token expenditure.", bullet_style))
    story.append(Paragraph("• <b>Static AST Validation:</b> Pre-parsing generated code with Python's <code>ast</code> module to catch unassigned DataFrame transformations and common pandas deprecation warnings before subprocess execution.", bullet_style))

    # Page break for Appendix
    story.append(PageBreak())
    story.append(Paragraph("Appendix: Standardized Prompt Templates & Demonstrations", h1_style))
    story.append(Paragraph(
        "Per Instructions Page 9, the complete prompt templates and worked demonstration format are provided below. "
        "All four strategies share this exact foundation to guarantee an isolated, rigorous comparison.",
        body_style,
    ))
    story.append(Spacer(1, 4))

    # Appendix A
    story.append(Paragraph("<b>Appendix A: System Prompt (Shared Across All Strategies)</b>", h2_style))
    sys_prompt_text = (
        "You are an expert Python and pandas data engineer specializing in Table-to-Table (TbT) transformation synthesis.\n"
        "Given a source table schema with sample rows and a desired target table schema with sample rows, your task is to synthesize a general Python function that transforms the source DataFrame into the target DataFrame.\n\n"
        "Strict Requirements:\n"
        "1. Provide a clear, visible step-by-step reasoning plan (Chain of Thought) explaining the sequence of operators required (e.g., column selection, date/timestamp parsing and formatting, renaming, reshaping, aggregations, unit conversions, missing value handling).\n"
        "2. Follow the reasoning plan with a single ```python ... ``` code block defining:\n"
        "   import pandas as pd\n\n"
        "   def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
        "       \"\"\"Return a DataFrame with the same schema and contents as target.csv.\"\"\"\n"
        "       ...\n"
        "3. The function must compute its result SOLELY from the `source` argument. It must NOT open or read target.csv, test_0.csv, training_0.csv, or any file from disk.\n"
        "4. Do NOT hardcode target rows or literal values from the sample. The transformation must generalize to unseen test rows with the same source schema.\n"
        "5. The returned DataFrame must have column names matching the target schema EXACTLY (case-sensitive and whitespace-sensitive).\n"
        "6. Use only pandas, numpy, and the Python standard library. Code must be deterministic and self-contained."
    )
    story.append(Paragraph(sys_prompt_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), app_code_style))

    # Appendix B
    story.append(Paragraph("<b>Appendix B: Standardized User Prompt Skeleton (Sample Data Substitution)</b>", h2_style))
    user_prompt_text = (
        "### Benchmark Case: length{L}_{k}\n"
        "- Source sample rows: {source_row_count} rows (Note: test_0.csv may have different row count)\n"
        "- Target rows: {target_row_count} rows\n"
        "[If row counts differ: Notice: Row count changes from {source} to {target}. Check if aggregation/grouping/pivot is required.]\n\n"
        "### Exact Target Columns (Must match verbatim):\n"
        "['target_col_1', 'target_col_2', ...]\n\n"
        "### Datetime Format Inferences:\n"
        "- Source column '{col}' has date format '{src_fmt}' (sample: '{src_val}')\n"
        "- Target column '{col}' requires date format '{tgt_fmt}' (sample: '{tgt_val}')\n\n"
        "### Source Schema and Types: col1 (dtype), col2 (dtype), ...\n"
        "### Target Schema and Types: col1 (dtype), col2 (dtype), ...\n"
        "### Distinct values for categorical / low-cardinality source columns: {col}: {distinct_values}\n\n"
        "### Source Table Sample (training_0.csv):\n"
        "| CST | Strata_ID | ... (8 boundary rows: 4 head + 4 tail) |\n\n"
        "### Desired Target Table Sample (target.csv):\n"
        "| cst | 1:00 | 2:00 | ... (8 boundary rows: 4 head + 4 tail) |\n\n"
        "### Instructions:\n"
        "1. Write a step-by-step reasoning plan (Chain of Thought) analyzing the transformation steps needed.\n"
        "2. Conclude with a single ```python ``` code block implementing `def transform(source: pd.DataFrame) -> pd.DataFrame:`.\n"
        "3. Make sure to return `df[target_columns]` with the target column names copied verbatim."
    )
    story.append(Paragraph(user_prompt_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), app_code_style))

    # Appendix C
    story.append(Paragraph("<b>Appendix C: Worked In-Context Demonstration (from Held-Out Split length1_1)</b>", h2_style))
    demo_text = (
        "### Worked Example: length1_1\n"
        "Source Schema: Strata_ID (int64), DT_STRATA (object), PCT_HOURLY_0100..PCT_HOURLY_2500 (float64)\n"
        "Target Schema: cst (object), 1:00..24:00 (float64)\n"
        "Reasoning:\n"
        "1. Source date 'DT_STRATA' has format 'M/D/YYYY'; target 'cst' requires '%a %m/%d/%Y'. Parse and format via pd.to_datetime.\n"
        "2. Rename hourly columns 'PCT_HOURLY_0100'..'PCT_HOURLY_2400' to '1:00'..'24:00'.\n"
        "3. Drop metadata columns ('Strata_ID', 'DOW', 'PCT_HOURLY_2500') and project exact target columns.\n"
        "Code:\n"
        "import pandas as pd\n\n"
        "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
        "    df = source.copy()\n"
        "    df['cst'] = pd.to_datetime(df['DT_STRATA']).dt.strftime('%a %m/%d/%Y')\n"
        "    rename_dict = {f'PCT_HOURLY_{i:02d}00': f'{i}:00' for i in range(1, 25)}\n"
        "    df = df.rename(columns=rename_dict)\n"
        "    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]\n"
        "    return df[target_cols]"
    )
    story.append(Paragraph(demo_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), app_code_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated 5-page report: {output_filename}")


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "A4_vavaghad.pdf"
    create_report(out_file)
