// Papatzis Engine Version: 1.4.0-embedded
use serde::{Deserialize, Serialize};

use std::env;
use std::fs;
use std::io::{Read, Write};
use std::path::PathBuf;
use std::process::{Command, Stdio};

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

#[derive(Serialize, Deserialize)]
struct SlopSettings {
    sensitivity: i32,
    experimental: bool,
    humanity_shield: bool,
}

#[derive(Serialize, Deserialize)]
struct SlopRequest {
    command: String,
    content: String,
    language: String,
    file_path: String,
    settings: SlopSettings,
}

#[cfg(target_os = "windows")]
const SIDECAR_BYTES: &[u8] = include_bytes!("../binaries/slop-engine-x86_64-pc-windows-msvc.exe");

#[cfg(target_os = "windows")]
fn extract_sidecar() -> Result<PathBuf, String> {
    let mut path = env::temp_dir();
    path.push("papatzis_engine_v1.4.0_embedded.exe");
    
    // Only write if it doesn't exist or is empty
    if !path.exists() || fs::metadata(&path).map(|m| m.len()).unwrap_or(0) == 0 {
        fs::write(&path, SIDECAR_BYTES).map_err(|e| format!("Failed to extract engine: {}", e))?;
    }
    
    Ok(path)
}

#[cfg(not(target_os = "windows"))]
fn extract_sidecar() -> Result<PathBuf, String> {
    Err("Only Windows is supported for the embedded sidecar.".to_string())
}

#[tauri::command]
fn analyze_code(code: String, language: String, settings: SlopSettings) -> Result<String, String> {
    let sidecar_path = extract_sidecar()?;

    #[cfg(target_os = "windows")]
    let mut cmd = {
        let mut c = Command::new(sidecar_path);
        c.creation_flags(0x08000000); // CREATE_NO_WINDOW
        c
    };

    #[cfg(not(target_os = "windows"))]
    let mut cmd = Command::new(sidecar_path);

    let mut child = cmd
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn engine: {}", e))?;

    let request = SlopRequest {
        command: "analyze".into(),
        content: code,
        language,
        file_path: "editor".into(),
        settings,
    };
    let json_req = serde_json::to_string(&request).unwrap();

    // Write to stdin
    if let Some(mut stdin) = child.stdin.take() {
        stdin.write_all(format!("{}\n", json_req).as_bytes()).map_err(|e| e.to_string())?;
    } else {
        return Err("Failed to open stdin".to_string());
    }

    let mut output = String::new();
    if let Some(mut stdout) = child.stdout.take() {
        stdout.read_to_string(&mut output).map_err(|e| e.to_string())?;
    }

    let mut err_output = String::new();
    if let Some(mut stderr) = child.stderr.take() {
        stderr.read_to_string(&mut err_output).ok();
    }

    let status = child.wait().map_err(|e| e.to_string())?;

    if status.success() {
        Ok(output)
    } else {
        Err(format!("Engine failed: {}\nOutput: {}", err_output, output))
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .invoke_handler(tauri::generate_handler![analyze_code])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
