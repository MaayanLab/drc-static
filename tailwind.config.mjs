/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	// theme: {
	// 	extend: {
	// 		colors: {
	// 			'primary': 'rgb(45, 89, 134)', # secondary-main
	// 			'secondary': 'rgb(219, 237, 240)', # primary light
	// 		}
	// 	},
	// },
	theme: {
    extend: {
		colors: {
			primary: {
			  main: '#C3E1E6',
			  light: '#DBEDF0',
			  dark: '#84A9AE'
			},
			secondary: {
			  main: '#2D5986',
			  light: '#9cbcde',
			  dark: '#122436'
			},
			tertiary: {
			  main: '#2D5986',
			  light: '#9cbcde',
			  dark: '#122436'
			},
			paperGray: {
			  main: '#FAFAFA',
			  light: '#fdfdfd',
			  dark: '#afafaf'
			},
		},
      fontSize: {
        'h1': '40px',
        'h2': '32px',
        'h3': '24px',
        'h4': '22px',
        'h5': '20px',
        'cfde': '40px',
        'cfde-small': '24px',
        'subtitle1': '16px',
        'subtitle2': '15px',
        'body1': '16px',
        'body2': '15px',
        'caption': '14px',
        'nav': '16px',
        'footer': '16px',
        'stats-h3': '24px',
        'stats-sub': '16px',
        'stats-sub-small': '14px'
      },
      fontWeight: {
        normal: 400,
        medium: 500,
        semibold: 600,
		bold: 700
      },
      fontFamily: {
        'hanken': ['Hanken Grotesk', 'serif'],
        'dm-sans': ['DM Sans', 'serif']
      },
      borderRadius: {
        'chip': '120px'
      },
      padding: {
        'btn': '8px 16px',
        'chip': '10px 16px'
      },
      backgroundColor: {
        'app-bar': '#FFF'
      },
      boxShadow: {
        'app-bar': 'none'
      },
      textColor: {
        'nav': '#2D5986',
        'stats': '#9E9E9E'
      }
    }
  },
	plugins: [
		require('@tailwindcss/typography'),
		
	],
	//  plugins: [
	// 	plugin(function({ addComponents }) {
	// 	  addComponents({
	// 		// Titles and Headers
	// 		'.title': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '40px',
	// 		  fontWeight: '500',
	// 		  textTransform: 'uppercase',
	// 		},
	// 		'.title-small': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '24px',
	// 		  fontWeight: '500',
	// 		  textTransform: 'uppercase',
	// 		},
	// 		'h1': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '40px',
	// 		  fontWeight: '500',
	// 		},
	// 		'h2': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '32px',
	// 		  fontWeight: '500',
	// 		},
	// 		'h3': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '24px',
	// 		  fontWeight: '500',
	// 		},
	// 		// Body text
	// 		'.body1': {
	// 		  fontFamily: 'DM Sans, sans-serif',
	// 		  fontSize: '16px',
	// 		  fontWeight: '500',
	// 		},
	// 		'.nav': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '16px',
	// 		  fontWeight: '600',
	// 		  textTransform: 'uppercase',
	// 		  color: '#2D5986',
	// 		},
	// 		// Stats
	// 		'.stats-h3': {
	// 		  fontFamily: 'Hanken Grotesk, sans-serif',
	// 		  fontSize: '24px',
	// 		  fontWeight: '500',
	// 		  color: '#9E9E9E',
	// 		}
	// 	  })
	// 	})
	//   ],
	}
