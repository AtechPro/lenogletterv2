document.addEventListener('DOMContentLoaded', () => {
    const documentCheckboxes = document.getElementById('document-checkboxes');
    const addDocumentBtn = document.getElementById('add-document-btn');
    const newDocumentInput = document.getElementById('new-document');
    const notification = document.getElementById('notification');
    const form = document.querySelector('form');

    // Predetermined documents
    const predeterminedDocuments = [
        "Cover letter for technical proposal",
        "Exhibit I (Scope of Work)",
        "Exhibit III (Unpriced schedule of rates)",
        "HSE Documents",
        "Key Personnel CV / Resume",
        "Company Experience",
        "Letter of compliance to Scope of Work",
        "Letter of compliance to Terms and Condition of Contracts",
        "Agency Letter"
    ];

    // Function to show notifications
    function showNotification(message) {
        notification.textContent = message;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Function to add a document to the form
    function addDocumentToForm(docValue, autoCheck = false) {
        const docId = `doc-${Date.now()}`;

        // Create new checkbox item
        const checkboxDiv = document.createElement('div');
        checkboxDiv.className = 'checkbox-item';
        checkboxDiv.setAttribute('draggable', 'true');
        checkboxDiv.dataset.value = docValue;
        checkboxDiv.style.display = 'flex'; // Add flexbox
        checkboxDiv.style.alignItems = 'center'; // Center items vertically
        checkboxDiv.style.width = '100%'; // Ensure it takes full width

        // Create drag handle
        const dragHandle = document.createElement('span');
        dragHandle.className = 'drag-handle';
        dragHandle.textContent = '☰';

        // Create the input element
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'documents[]';
        checkbox.value = docValue;
        checkbox.id = docId;
        checkbox.checked = autoCheck;

        // Create the label
        const label = document.createElement('label');
        label.htmlFor = docId;
        label.textContent = docValue;
        label.style.flexGrow = '1'; // This allows the label to take available space

        // Create delete button with improved styling
        const deleteButton = document.createElement('span');
        deleteButton.className = 'delete-btn';
        deleteButton.innerHTML = '&times;'; // Using × symbol instead of − (minus)
        deleteButton.style.marginLeft = 'auto'; // This pushes it to the right
        deleteButton.style.cursor = 'pointer';
        deleteButton.style.color = '#ff4d4f'; // Red color for delete
        deleteButton.style.fontWeight = 'bold';
        deleteButton.style.fontSize = '18px';
        deleteButton.style.padding = '0 8px';
        deleteButton.style.borderRadius = '50%';
        deleteButton.style.transition = 'background-color 0.2s';
        deleteButton.addEventListener('mouseover', () => {
            deleteButton.style.backgroundColor = '#fff1f0';
        });
        deleteButton.addEventListener('mouseout', () => {
            deleteButton.style.backgroundColor = '';
        });
        deleteButton.onclick = () => {
            checkboxDiv.remove(); // Remove the document from the DOM
            saveDocuments(); // Save the updated list to localStorage
            showNotification('Document deleted successfully!');
        };

        // Append elements to the checkboxDiv
        checkboxDiv.appendChild(dragHandle);
        checkboxDiv.appendChild(checkbox);
        checkboxDiv.appendChild(label);
        checkboxDiv.appendChild(deleteButton);

        // Add the new document to the top of the list
        documentCheckboxes.prepend(checkboxDiv); // Use prepend instead of append

        // Highlight the new document briefly
        checkboxDiv.style.backgroundColor = '#e6f7ff';
        setTimeout(() => {
            checkboxDiv.style.backgroundColor = '';
        }, 1000);
    }

    // Function to load documents from localStorage
    function loadDocuments() {
        const savedDocuments = JSON.parse(localStorage.getItem('documents')) || [];
        const allDocuments = [...new Set([...predeterminedDocuments, ...savedDocuments])];
        allDocuments.forEach(doc => {
            addDocumentToForm(doc);
        });
    }

    // Function to save documents to localStorage
    function saveDocuments() {
        const checkboxes = document.querySelectorAll('#document-checkboxes .checkbox-item input[type="checkbox"]');
        const documents = [];
        checkboxes.forEach(checkbox => {
            documents.push(checkbox.value);
        });
        localStorage.setItem('documents', JSON.stringify(documents));
    }

    // Function to handle adding a new document
    function handleAddDocument() {
        const docValue = newDocumentInput.value.trim();
        if (docValue === '') {
            showNotification('Please enter a valid document name.');
            return;
        }

        // Check for duplicates
        const existingCheckboxes = document.querySelectorAll('#document-checkboxes input[type="checkbox"]');
        const isDuplicate = Array.from(existingCheckboxes).some(checkbox => checkbox.value === docValue);
        if (isDuplicate) {
            showNotification('This document already exists in the list.');
            return;
        }

        // Add the new document to the form and auto-check it
        addDocumentToForm(docValue, true);

        // Save the updated list to localStorage
        saveDocuments();

        // Clear the input field
        newDocumentInput.value = '';

        showNotification('Document added successfully!');
    }

    // Function to handle form submission
    function handleFormSubmit(event) {
        const selectedDocuments = document.querySelectorAll('#document-checkboxes input[type="checkbox"]:checked');
        if (selectedDocuments.length === 0) {
            event.preventDefault();
            showNotification('Please select at least one document.');
        }
    }

    // Initialize the form with predetermined documents
    loadDocuments();

    // Event listener for adding a new document
    addDocumentBtn.addEventListener('click', handleAddDocument);

    // Allow pressing Enter to add the document
    newDocumentInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleAddDocument();
        }
    });

    // Event listener for form submission
    form.addEventListener('submit', handleFormSubmit);

    // Drag and Drop Functionality
    let draggedItem = null;

    documentCheckboxes.addEventListener('dragstart', (e) => {
        if (e.target.classList.contains('checkbox-item')) {
            draggedItem = e.target;
            setTimeout(() => {
                e.target.style.display = 'none';
            }, 0);
        }
    });

    documentCheckboxes.addEventListener('dragend', (e) => {
        setTimeout(() => {
            draggedItem.style.display = 'flex'; // Change to flex to maintain layout
            draggedItem = null;
        }, 0);
    });

    documentCheckboxes.addEventListener('dragover', (e) => {
        e.preventDefault();
        const hoveringItem = e.target;
        if (hoveringItem.classList.contains('checkbox-item')) {
            const bounding = hoveringItem.getBoundingClientRect();
            const offset = bounding.top + bounding.height / 2;
            if (e.clientY > offset) {
                documentCheckboxes.insertBefore(draggedItem, hoveringItem.nextElementSibling);
            } else {
                documentCheckboxes.insertBefore(draggedItem, hoveringItem);
            }
        }
    });

    // Accessibility: Allow keyboard reordering
    documentCheckboxes.addEventListener('keydown', (e) => {
        const currentItem = e.target.closest('.checkbox-item');
        if (currentItem) {
            let newIndex;
            switch (e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    newIndex = Array.from(documentCheckboxes.children).indexOf(currentItem) - 1;
                    if (newIndex >= 0) {
                        documentCheckboxes.insertBefore(currentItem, documentCheckboxes.children[newIndex]);
                        saveDocuments();
                    }
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    newIndex = Array.from(documentCheckboxes.children).indexOf(currentItem) + 1;
                    if (newIndex < documentCheckboxes.children.length) {
                        documentCheckboxes.insertBefore(currentItem, documentCheckboxes.children[newIndex + 1]);
                        saveDocuments();
                    }
                    break;
                default:
                    break;
            }
        }
    });

    // Save documents when reordering is done
    documentCheckboxes.addEventListener('dragover', () => {
        saveDocuments();
    });
});