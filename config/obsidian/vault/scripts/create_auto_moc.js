/**
 * Auto-MOC Updater
 * Scans the Vault for tags/folders and updates Map of Content files.
 * Intended to be run via Templater or QuickAdd.
 */
async function update_moc(tp) {
    const files = app.vault.getMarkdownFiles();
    let moc_content = "# Auto-Generated MOC\n\n";

    // Example: List all files in 'ph' folder
    const ph_files = files.filter(f => f.path.startsWith("ph/"));
    
    moc_content += "## Project Phases\n";
    ph_files.forEach(f => {
        moc_content += `- [[${f.basename}]]\n`;
    });

    return moc_content;
}
module.exports = update_moc;
