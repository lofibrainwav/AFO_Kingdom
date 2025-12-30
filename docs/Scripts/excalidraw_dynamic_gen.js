/**
 * Scripts/excalidraw_dynamic_gen.js
 * ExcalidrawAutomate를 활용한 동적 다이어그램 생성
 */
module.exports = async function excalidraw_dynamic_gen(tp) {
    const ea = ExcalidrawAutomate;
    if (!ea) {
        new Notice("ExcalidrawAutomate not found! ⚠️");
        return;
    }
    
    try {
        ea.reset();
        const input = await tp.system.prompt("Data points (comma sep)?");
        if (!input) return;
        
        const data = input.split(',');
        data.forEach((item, i) => {
            ea.addText(100 * i, 0, item.trim());
        });
        
        const fileName = "Dynamic_Diagram_" + tp.date.now("YYYY-MM-DD");
        await ea.create({filename: fileName, foldername: "diagrams"});
        
        new Notice(`Diagram ${fileName} generated! 🎨`);
        return `![[${fileName}]]`;
    } catch (error) {
        console.error("Excalidraw Gen Error:", error);
        new Notice(`Excalidraw Error: ${error.message} ⚠️`);
    }
}
