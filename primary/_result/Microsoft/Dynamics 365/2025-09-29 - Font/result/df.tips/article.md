# My solutions
# 1.
The online version of Business Central (`BC`) **does not natively support** the «Century Gothic» (`CG`) font for report generation: [learn.microsoft.com/en-us/dynamics365/business-central/ui-fonts#document-fonts](https://learn.microsoft.com/en-us/dynamics365/business-central/ui-fonts#document-fonts)
# 2.
There are **3 viable solutions** to your task.  
I describe them in **points 3-5** below.
# 3. Solution 1: A font can be embedded into a Word report layout
Note: This method only works with Word layouts; if the report currently uses an RDLC layout, this method cannot be applied directly.
## 3.1. Step-by-step instructions
### 3.1.1.
In `BC`, navigate to the «**Report Layout Selection**» (`RLS`) page and locate the required report.
### 3.1.2. 
Choose the «**Custom Layouts**» action (often found under the «**Process**» or «**Actions**» menu) to open the «**Custom Report Layouts**» (`CRL`) page.
### 3.1.3. 
As built-in layouts cannot be modified, create a new custom Word layout (`L`) based on an existing layout.
### 3.1.4. 
Choose the «**New**» action.
### 3.1.5.
In the dialog box that appears, ensure the «**Insert Word Layout**» toggle is activated and choose «**OK**» to create a copy of the built-in Word layout.
### 3.1.6. 
Select `L` and choose the «**Layout**» → «**Export Layout**» action to save it as a `.docx` file (`F`).
### 3.1.7. 
Open `F` in Microsoft Word (`W`).
### 3.1.8. 
Apply `CG` to the necessary text fields and content controls.
### 3.1.9. 
In `W`, navigate to «**File**» → «**Options**» → «**Save**».
### 3.1.10. 
In the section «**Preserve fidelity when sharing this document**», configure the following settings.
### 3.1.11. 
Activate the «**Embed fonts in the file**» option.
### 3.1.12. 
To optimize the file size, activate the «**Embed only the characters used in the document (best for reducing file size)**» option.
### 3.1.13. 
Crucially, deactivate the «**Do not embed common system fonts**» option.   
This is necessary because the `BC` SaaS server-side component often fails to correctly render custom fonts if this option remains activated.
### 3.1.13. 
Save `F`.
### 3.1.15. 
Return to `CRL`.
### 3.1.16. 
Select `L` and choose the «**Layout**» → «**Import Layout**» action to upload the modified file `F`.
### 3.1.17. 
Return to the `RLS` page.
### 3.1.18. 
On the `RLS` page, locate the report and set the «**Selected Layout**» field to «**Custom Layout**».
### 3.1.19. 
In the «**Custom Layout Description**» field, select the layout `L`.
## 3.2. Technical rationale
### 3.2.1. 
The success of this method depends on the PDF file generation process on the `BC` server.
### 3.2.2. 
When the system generates a PDF from a Word layout, it uses a server-side component (the Aspose library).
### 3.2.3. 
If the font is not embedded in the `.docx` file, the component reads the font name and attempts to locate it in the list of fonts installed on the server.   
If the font is not found, the component substitutes it with a default fallback font.   
This substitution is the cause of the issue you are experiencing.
### 3.2.4. 
When the embedding option is activated, complete information about the font's glyphs and metrics is saved directly inside the `.docx` file.   
This allows the server-side component to extract the font data from the document itself and use it to correctly render the text in the PDF, even if the font is not installed in the server's operating system.
## 3.3. 
Method #1 requires the font's «**Font Embeddability**» property to have the value «**Editable**» or «**Installable**».  
I have verified that `CG` meets this requirement (it is «**Installable**»): see the attached file `Century Gothic.png`.
# 4. Solution 2: Using a third-party extension for advanced reporting (ForNAV)
A key feature of ForNAV is its built-in and officially supported capability to work with custom fonts.  
Font embedding in ForNAV is a core, documented feature of the extension itself.  
The ForNAV Designer automatically detects when a locally installed custom font is used in the layout and embeds its data directly into the report layout file when the layout is saved.  
ForNAV's native rendering service, which processes these layouts in the `BC` environment, is specifically designed to work correctly with such embedded fonts.  
This ensures a stable and predictable result, completely eliminating the uncertainty and risks associated with the standard `BC` rendering component.
# 5. Solution 3: Developing an external microservice (e.g., Azure Function)
This approach involves creating a separate service to handle PDF generation outside of the standard `BC` environment.  
`BC` sends the report data (JSON/XML) to this service.  
The service, using third-party PDF generation libraries (e.g., PDFSharp, IronPDF) that support full font embedding, generates the document with `CG` and returns it to `BC`.  
This method guarantees the use of any font and complex formatting, bypassing `BC`'s rendering limitations, and generates a high-quality PDF with embedded text (searchable and copyable).