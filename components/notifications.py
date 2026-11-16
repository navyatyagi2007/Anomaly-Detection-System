
import streamlit as st

def render_notifications():

    col1, col2 = st.columns([10, 1])

    with col2:
        with st.popover("🔔", use_container_width=True):

            st.markdown("### Notifications")

            st.markdown("---")

            st.error(
                "🔴 Critical Alert\n\n"
                "M-07 Air Compressor: Bearing wear detected."
            )

            st.warning(
                "🟠 Maintenance Reminder\n\n"
                "M-04 CNC Mill: Inspection due soon."
            )

            st.info(
                "🔵 AI Update\n\n"
                "New anomaly detected in Machine M-10."
            )

            st.markdown("---")

            if st.button("Mark all as read"):
                st.success("Notifications marked as read.")
