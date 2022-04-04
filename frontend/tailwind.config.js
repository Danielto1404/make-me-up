module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            boxShadow: {
                "neon": "0px 0px 8px 2px  rgba(255, 255, 255, 1)",
                "gray-input": "0px 0px 8px 0px rgba(4, 17, 29, 0.25)",
            },
            colors: {
                "gradient-from": '#9ED8DB',
                "gradient-to": "#007B82",
                'green-d': 'rgb(44, 64, 73)',
                'input-focused': '#fbfdff',
            }
        },
    },
    plugins: [],
}
