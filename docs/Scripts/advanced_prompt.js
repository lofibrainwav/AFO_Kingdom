/**
 * Scripts/advanced_prompt.js
 * (tp.user.advanced_prompt(tp) 호출)
 */
module.exports = async function advanced_prompt(tp) {
  try {
    const config = {
      title: { prompt: "Title?", value: tp.file.title },
      tags: { prompt: "Tags (comma separated)?", value: [], multiline: true }
    };
    
    for (const key in config) {
      const input = await tp.system.prompt(config[key].prompt, config[key].value || "");
      
      // 사용자 취소 시 (Esc 등) 실행 중단
      if (input === null) {
        new Notice("Template generation cancelled by user. 🛑");
        return "<!-- Template insertion cancelled -->";
      }
      
      if (key === "tags") {
          config[key].value = input.split(',').map(s => s.trim()).filter(s => s !== "");
      } else {
          config[key].value = input;
      }
    }
    
    return `---\ntitle: ${config.title.value}\ntags: [${config.tags.value.join(', ')}]\n---`;
  } catch (error) {
    console.error("Advanced Prompt Error:", error);
    new Notice(`Prompt Error: ${error.message} ⚠️`);
    return `%% Error: ${error.message} %%`;
  }
}
