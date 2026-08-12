import streamlit as st
import pandas as pd
from datetime import datetime

from database import (
    get_notes,
    add_note,
    delete_note,
    update_note
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Notes Manager",
    page_icon="📝",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("📝 Notes Manager")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
    "Dashboard",
    "Notes",
    "Search & Filter",
    "Analysis",
    "Visualization",
    "AI Features"
]
)

st.sidebar.divider()

st.sidebar.info(
    "Python • MySQL • Streamlit • Groq AI"
)

st.sidebar.divider()

st.sidebar.caption(
    "📝 Notes Manager"
)

st.sidebar.caption(
    "Python + MySQL + Streamlit + Groq AI"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📝 Notes Manager")

st.write(
    "Manage, analyze and explore your notes using a MySQL-powered application."
)

st.divider()


# --------------------------------------------------
# LOAD NOTES FROM MYSQL
# --------------------------------------------------

notes = get_notes()

if notes:

    df = pd.DataFrame(notes)

else:

    df = pd.DataFrame(
        columns=[
            "id",
            "title",
            "category",
            "priority",
            "status",
            "source",
            "content",
            "date_created",
            "last_modified"
        ]
    )


# --------------------------------------------------
# DASHBOARD KPIs
# --------------------------------------------------

total_notes = len(df)

active_notes = len(
    df[df["status"] == "Active"]
) if not df.empty else 0

completed_notes = len(
    df[df["status"] == "Completed"]
) if not df.empty else 0

ai_notes = len(
    df[df["source"] == "AI"]
) if not df.empty else 0


if page == "Dashboard":

    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📝 Total Notes",
            value=total_notes
        )

    with col2:
        st.metric(
            label="🟢 Active Notes",
            value=active_notes
        )

    with col3:
        st.metric(
            label="✅ Completed Notes",
            value=completed_notes
        )

    with col4:
        st.metric(
            label="🤖 AI Notes",
            value=ai_notes
        )

st.divider()

# --------------------------------------------------
# ANALYSIS REPORT
# --------------------------------------------------

if page == "Analysis":

    st.subheader("📊 Analysis Report")

    if df.empty:

        st.info("No notes available for analysis.")

    else:

        total = len(df)

        active = len(
            df[df["status"] == "Active"]
        )

        completed = len(
            df[df["status"] == "Completed"]
        )

        ai_count = len(
            df[df["source"] == "AI"]
        )

        manual_count = len(
            df[df["source"] == "Manual"]
        )

        st.write("### 📌 Overall Statistics")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Notes", total)

        with col2:
            st.metric("Active", active)

        with col3:
            st.metric("Completed", completed)

        with col4:
            st.metric("AI Notes", ai_count)

        with col5:
            st.metric("Manual Notes", manual_count)


        st.divider()

        st.write("### 📂 Category Analysis")

        category_counts = (
            df["category"]
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            "Category",
            "Count"
        ]

        st.dataframe(
            category_counts,
            use_container_width=True,
            hide_index=True
        )


        st.write("### ⭐ Priority Analysis")

        priority_counts = (
            df["priority"]
            .value_counts()
            .reset_index()
        )

        priority_counts.columns = [
            "Priority",
            "Count"
        ]

        st.dataframe(
            priority_counts,
            use_container_width=True,
            hide_index=True
        )


        st.write("### 📌 Status Analysis")

        status_counts = (
            df["status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        st.dataframe(
            status_counts,
            use_container_width=True,
            hide_index=True
        )


        st.write("### 🤖 AI vs Manual")

        source_counts = (
            df["source"]
            .value_counts()
            .reset_index()
        )

        source_counts.columns = [
            "Source",
            "Count"
        ]

        st.dataframe(
            source_counts,
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# VISUALIZATION REPORT
# --------------------------------------------------

if page == "Visualization":

    st.subheader("📈 Visualization Report")

    if df.empty:

        st.info("No notes available for visualization.")

    else:

        st.write("### 📂 Notes by Category")

        category_counts = (
            df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )


        st.write("### ⭐ Notes by Priority")

        priority_counts = (
            df["priority"]
            .value_counts()
        )

        st.bar_chart(
            priority_counts
        )


        st.write("### 📌 Notes by Status")

        status_counts = (
            df["status"]
            .value_counts()
        )

        st.bar_chart(
            status_counts
        )


        st.write("### 🤖 AI vs Manual Notes")

        source_counts = (
            df["source"]
            .value_counts()
        )

        st.bar_chart(
            source_counts
        )

# --------------------------------------------------
# NOTES PAGE
# --------------------------------------------------

if page == "Notes":

    # --------------------------------------------------
    # VIEW NOTES
    # --------------------------------------------------

    st.subheader("📋 All Notes")

    if df.empty:

        st.info("No notes found in the database.")

    else:

        display_df = df[
            [
                "id",
                "title",
                "category",
                "priority",
                "status",
                "source",
                "date_created",
                "last_modified"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # NOTE DETAILS
        # --------------------------------------------------

        st.divider()

        st.subheader("🔎 Note Details")

        selected_id = st.selectbox(
            "Select Note ID",
            df["id"].tolist(),
            key="details_note_id"
        )

        selected_note = df[
            df["id"] == selected_id
        ].iloc[0]

        st.write(
            f"### {selected_note['title']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                f"**Category:** {selected_note['category']}"
            )

        with col2:
            st.write(
                f"**Priority:** {selected_note['priority']}"
            )

        with col3:
            st.write(
                f"**Status:** {selected_note['status']}"
            )

        st.write(
            f"**Source:** {selected_note['source']}"
        )

        st.write("### Content")

        st.write(
            selected_note["content"]
        )

        # --------------------------------------------------
        # ADD NOTE
        # --------------------------------------------------

        st.divider()

        st.subheader("➕ Add New Note")

        with st.form("add_note_form"):

            title = st.text_input(
                "Title"
            )

            category = st.text_input(
                "Category"
            )

            priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
                key="manual_priority"
            )

            status = st.selectbox(
                "Status",
                ["Active", "Completed"],
                key="manual_status"
            )

            source = st.selectbox(
                "Source",
                ["Manual", "AI"],
                key="manual_source"
            )

            content = st.text_area(
                "Note Content",
                height=150
            )

            submitted = st.form_submit_button(
                "Add Note"
            )

            if submitted:

                if (
                    not title.strip()
                    or not content.strip()
                ):

                    st.warning(
                        "Title and content cannot be empty."
                    )

                else:

                    today = datetime.now().strftime(
                        "%Y-%m-%d"
                    )

                    new_note = {
                        "title": title,
                        "category": category,
                        "priority": priority,
                        "status": status,
                        "source": source,
                        "content": content,
                        "date_created": today,
                        "last_modified": today
                    }

                    add_note(new_note)

                    st.success(
                        "✅ Note added successfully!"
                    )

                    st.rerun()

        # --------------------------------------------------
        # UPDATE NOTE
        # --------------------------------------------------

        st.divider()

        st.subheader("✏️ Update Note")

        update_id = st.selectbox(
            "Select Note ID to Update",
            df["id"].tolist(),
            key="update_note_id"
        )

        selected_update_note = df[
            df["id"] == update_id
        ].iloc[0]

        with st.form("update_note_form"):

            update_title = st.text_input(
                "Title",
                value=selected_update_note["title"]
            )

            update_category = st.text_input(
                "Category",
                value=selected_update_note["category"]
            )

            update_priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
                index=[
                    "High",
                    "Medium",
                    "Low"
                ].index(
                    selected_update_note["priority"]
                ),
                key="update_priority"
            )

            update_status = st.selectbox(
                "Status",
                ["Active", "Completed"],
                index=[
                    "Active",
                    "Completed"
                ].index(
                    selected_update_note["status"]
                ),
                key="update_status"
            )

            update_source = st.selectbox(
                "Source",
                ["Manual", "AI"],
                index=[
                    "Manual",
                    "AI"
                ].index(
                    selected_update_note["source"]
                ),
                key="update_source"
            )

            update_content = st.text_area(
                "Content",
                value=selected_update_note["content"],
                height=150
            )

            update_button = st.form_submit_button(
                "✏️ Update Note"
            )

            if update_button:

                update_note(
                    update_id,
                    update_title,
                    update_category,
                    update_priority,
                    update_status,
                    update_source,
                    update_content
                )

                st.success(
                    "✅ Note updated successfully!"
                )

                st.rerun()

        # --------------------------------------------------
        # DELETE NOTE
        # --------------------------------------------------

        st.divider()

        st.subheader("🗑️ Delete Note")

        delete_id = st.selectbox(
            "Select Note ID to Delete",
            df["id"].tolist(),
            key="delete_note_id"
        )

        if st.button(
            "🗑️ Delete Note",
            type="primary"
        ):

            delete_note(delete_id)

            st.success(
                "✅ Note deleted successfully!"
            )

            st.rerun()

        # --------------------------------------------------
        # CHANGE NOTE STATUS
        # --------------------------------------------------

        st.divider()

        st.subheader("🔄 Change Note Status")

        status_note_id = st.selectbox(
            "Select Note ID",
            df["id"].tolist(),
            key="status_note_id"
        )

        selected_status_note = df[
            df["id"] == status_note_id
        ].iloc[0]

        st.write(
            f"Current Status: **{selected_status_note['status']}**"
        )

        new_status = st.selectbox(
            "New Status",
            ["Active", "Completed"],
            key="change_status"
        )

        if st.button(
            "🔄 Update Status"
        ):

            update_note(
                status_note_id,
                selected_status_note["title"],
                selected_status_note["category"],
                selected_status_note["priority"],
                new_status,
                selected_status_note["source"],
                selected_status_note["content"]
            )

            st.success(
                f"✅ Status changed to {new_status}!"
            )

            st.rerun()

# --------------------------------------------------
# SEARCH & FILTER
# --------------------------------------------------

if page == "Search & Filter":

    # --------------------------------------------------
    # SEARCH NOTES
    # --------------------------------------------------

    st.subheader("🔎 Search Notes")

    search_text = st.text_input(
        "Search by title, category or content"
    )

    if search_text.strip():

        search_value = search_text.lower()

        search_results = df[
            df["title"].fillna("").str.lower().str.contains(
                search_value,
                na=False
            )
            |
            df["category"].fillna("").str.lower().str.contains(
                search_value,
                na=False
            )
            |
            df["content"].fillna("").str.lower().str.contains(
                search_value,
                na=False
            )
        ]

        if search_results.empty:

            st.warning(
                "No matching notes found."
            )

        else:

            st.dataframe(
                search_results[
                    [
                        "id",
                        "title",
                        "category",
                        "priority",
                        "status",
                        "source"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    else:

        st.info(
            "Enter a keyword to search notes."
        )


    # --------------------------------------------------
    # FILTER NOTES
    # --------------------------------------------------

    st.divider()

    st.subheader("🔽 Filter Notes")

    if not df.empty:

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            category_filter = st.selectbox(
                "Category",
                ["All"] + sorted(
                    df["category"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

        with col2:

            priority_filter = st.selectbox(
                "Priority",
                ["All", "High", "Medium", "Low"]
            )

        with col3:

            status_filter = st.selectbox(
                "Status",
                ["All", "Active", "Completed"]
            )

        with col4:

            source_filter = st.selectbox(
                "Source",
                ["All", "Manual", "AI"]
            )


        filtered_df = df.copy()


        if category_filter != "All":

            filtered_df = filtered_df[
                filtered_df["category"] == category_filter
            ]


        if priority_filter != "All":

            filtered_df = filtered_df[
                filtered_df["priority"] == priority_filter
            ]


        if status_filter != "All":

            filtered_df = filtered_df[
                filtered_df["status"] == status_filter
            ]


        if source_filter != "All":

            filtered_df = filtered_df[
                filtered_df["source"] == source_filter
            ]


        st.write(
            f"**{len(filtered_df)} note(s) found**"
        )


        st.dataframe(
            filtered_df[
                [
                    "id",
                    "title",
                    "category",
                    "priority",
                    "status",
                    "source",
                    "date_created"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No notes available for filtering."
        )
    
# --------------------------------------------------
# AI FEATURES
# --------------------------------------------------

if page == "AI Features":

    # --------------------------------------------------
    # AI NOTE GENERATION
    # --------------------------------------------------

    st.subheader("🤖 AI Note Generator")

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Python OOP"
    )

    if st.button("✨ Generate AI Note"):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            from ai_helper import generate_note

            with st.spinner("Generating note..."):

                generated_note = generate_note(topic)

            st.session_state["generated_note"] = generated_note
            st.session_state["generated_topic"] = topic


    if "generated_note" in st.session_state:

        st.write("### 📄 Generated Note")

        st.write(
            st.session_state["generated_note"]
        )

        st.write("### 💾 Save AI Note")

        with st.form("save_ai_note_form"):

            ai_title = st.text_input(
                "Title",
                value=st.session_state.get(
                    "generated_topic",
                    ""
                )
            )

            ai_category = st.text_input(
                "Category"
            )

            ai_priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
                key="ai_priority"
            )

            save_ai_note = st.form_submit_button(
                "Save AI Note"
            )

        if save_ai_note:

            from database import add_note
            from datetime import datetime

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            ai_note = {
                "title": ai_title,
                "category": ai_category,
                "priority": ai_priority,
                "status": "Active",
                "source": "AI",
                "content": st.session_state["generated_note"],
                "date_created": today,
                "last_modified": today
            }

            add_note(ai_note)

            st.success(
                "✅ AI Note saved successfully!"
            )

            st.session_state.pop(
                "generated_note",
                None
            )

            st.session_state.pop(
                "generated_topic",
                None
            )

            st.rerun()


    # --------------------------------------------------
    # AI NOTE SUMMARIZATION
    # --------------------------------------------------

    st.divider()

    st.subheader("📝 AI Note Summarizer")

    if not df.empty:

        summary_note_id = st.selectbox(
            "Select Note ID",
            df["id"].tolist(),
            key="summary_note_id"
        )

        selected_summary_note = df[
            df["id"] == summary_note_id
        ].iloc[0]

        st.write(
            f"**Title:** {selected_summary_note['title']}"
        )

        if st.button("✨ Generate Summary"):

            from ai_helper import summarize_note

            with st.spinner("Generating summary..."):

                summary = summarize_note(
                    selected_summary_note["content"]
                )

            st.session_state["generated_summary"] = summary


        if "generated_summary" in st.session_state:

            st.write("### 📄 AI Summary")

            st.write(
                st.session_state["generated_summary"]
            )

            if st.button(
                "💾 Save Summary as New Note"
            ):

                from database import add_note
                from datetime import datetime

                today = datetime.now().strftime(
                    "%Y-%m-%d"
                )

                summary_note = {
                    "title": selected_summary_note["title"] + " - Summary",
                    "category": selected_summary_note["category"],
                    "priority": selected_summary_note["priority"],
                    "status": "Active",
                    "source": "AI",
                    "content": st.session_state["generated_summary"],
                    "date_created": today,
                    "last_modified": today
                }

                add_note(summary_note)

                st.success(
                    "✅ Summary saved as a new note!"
                )

                st.session_state.pop(
                    "generated_summary",
                    None
                )

                st.rerun()

    else:

        st.info(
            "No notes available for summarization."
        )


    # --------------------------------------------------
    # AI QUIZ GENERATION
    # --------------------------------------------------

    st.divider()

    st.subheader("🧠 AI Quiz Generator")

    if not df.empty:

        quiz_note_id = st.selectbox(
            "Select Note ID",
            df["id"].tolist(),
            key="quiz_note_id"
        )

        selected_quiz_note = df[
            df["id"] == quiz_note_id
        ].iloc[0]

        st.write(
            f"**Title:** {selected_quiz_note['title']}"
        )

        if st.button("🧠 Generate Quiz"):

            from ai_helper import generate_quiz

            with st.spinner("Generating quiz..."):

                quiz = generate_quiz(
                    selected_quiz_note["content"]
                )

            st.session_state["generated_quiz"] = quiz


        if "generated_quiz" in st.session_state:

            st.write("### 📋 Generated Quiz")

            st.text(
                st.session_state["generated_quiz"]
            )

            if st.button(
                "💾 Save Quiz as Text File"
            ):

                file_name = f"Quiz_{quiz_note_id}.txt"

                with open(
                    file_name,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        st.session_state["generated_quiz"]
                    )

                st.success(
                    f"✅ Quiz saved successfully as {file_name}"
                )

    else:

        st.info(
            "No notes available for quiz generation."
        )