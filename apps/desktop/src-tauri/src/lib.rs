//! THEA desktop shell.
//!
//! Today: a native window that loads the THEA web UI (served by the home
//! server, or `pnpm dev:web` locally).
//!
//! Planned (docs/desktop.md):
//! - global push-to-talk shortcut and a tray icon
//! - start/stop the desktop bridge sidecar: a local MCP server on 127.0.0.1
//!   that lets the agent use this PC (open apps, read the screen, run
//!   commands), with every action confirmed in this window

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .run(tauri::generate_context!())
        .expect("error while running THEA desktop");
}
