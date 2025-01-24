/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				'primary': 'rgb(45, 89, 134)',
				'secondary': 'rgb(219, 237, 240)',
			}
		},
	},
	plugins: [
		require('@tailwindcss/typography'),
	],
}
