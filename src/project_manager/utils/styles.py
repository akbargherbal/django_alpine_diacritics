# utils/styles.py

STYLES = {
    "buttons": {
        # Primary button variations
        "primary": "bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50",
        "primary_sm": "bg-blue-500 hover:bg-blue-600 text-white font-medium py-1 px-3 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50",
        "primary_lg": "bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-6 rounded text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50",
        # Secondary button variations
        "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50",
        "secondary_sm": "bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-1 px-3 rounded text-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50",
        "secondary_lg": "bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-3 px-6 rounded text-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50",
        # Success button variations
        "success": "bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50",
        "success_sm": "bg-green-500 hover:bg-green-600 text-white font-medium py-1 px-3 rounded text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50",
        # Danger button variations
        "danger": "bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50",
        "danger_sm": "bg-red-500 hover:bg-red-600 text-white font-medium py-1 px-3 rounded text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50",
        # Warning button
        "warning": "bg-yellow-500 hover:bg-yellow-600 text-white font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-opacity-50",
        # Outline variations
        "outline": "border border-gray-300 hover:border-gray-400 text-gray-700 font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50",
        "outline_primary": "border border-blue-500 text-blue-500 hover:bg-blue-50 font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50",
    },
    "inputs": {
        # Text inputs
        "text": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50",
        "text_sm": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 text-sm",
        "text_error": "mt-1 block w-full rounded-md border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:ring-red-500",
        # Textarea
        "textarea": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 min-h-[100px]",
        # Select
        "select": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50",
        "select_sm": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 text-sm",
        # Checkbox and Radio
        "checkbox": "rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-offset-0 focus:ring-blue-200 focus:ring-opacity-50",
        "radio": "border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-offset-0 focus:ring-blue-200 focus:ring-opacity-50",
        # File input
        "file": """block w-full text-sm text-gray-500 
                  file:mr-4 file:py-2 file:px-4 
                  file:rounded-md file:border-0 
                  file:text-sm file:font-medium 
                  file:bg-blue-500 file:text-white 
                  hover:file:bg-blue-600 
                  focus:outline-none""",
    },
    "containers": {
        # Form containers
        "form_group": "space-y-4",
        "input_group": "mb-4",
        "button_group": "mt-4 flex justify-end space-x-2",
        "checkbox_group": "space-y-2",
        "radio_group": "space-y-2",
        # Grid layouts
        "grid_2": "grid grid-cols-1 md:grid-cols-2 gap-4",
        "grid_3": "grid grid-cols-1 md:grid-cols-3 gap-4",
    },
    "labels": {
        "default": "block text-sm font-medium text-gray-700",
        "required": 'block text-sm font-medium text-gray-700 after:content-["*"] after:ml-0.5 after:text-red-500',
        "error": "block text-sm font-medium text-red-700",
    },
    "help_text": {
        "default": "mt-1 text-sm text-gray-500",
        "error": "mt-1 text-sm text-red-600",
    },
}
