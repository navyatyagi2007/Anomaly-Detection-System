
"""ANOMATRIX Factory Illustration for Login Page."""

FACTORY_SVG = """
<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 760 390"
    width="1140"
    height="585"
>

<defs>

    <linearGradient id="b" x1="0" y1="0" x2="0" y2="1">
        <stop stop-color="#8DB8E8"/>
        <stop offset="1" stop-color="#5E91CA"/>
    </linearGradient>

    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
        <stop stop-color="#A9C9ED" stop-opacity=".3"/>
        <stop offset="1" stop-color="#5C91CE" stop-opacity=".7"/>
    </linearGradient>

</defs>


<!-- FACTORY BACKGROUND -->

<ellipse
    cx="420"
    cy="350"
    rx="390"
    ry="72"
    fill="#7CA9DC"
    opacity=".18"
/>

<path
    d="M0 326Q125 280 250 320T520 307T760 298V390H0Z"
    fill="url(#g)"
/>


<!-- BACKGROUND BUILDINGS -->

<g fill="#9BBCE3" opacity=".65">

    <path d="M35 286V230H80V208H130V286Z"/>

    <path d="M105 290V250H154V220H188V290Z"/>

    <path d="M570 300V240H620V215H666V300Z"/>

    <path d="M640 300V258H700V230H735V300Z"/>

</g>


<!-- MAIN FACTORY BUILDING -->

<path
    d="M115 300V194L190 154L265 194V170L335 132L405 170V300Z"
    fill="url(#b)"
/>

<path
    d="M115 194L190 154L265 194V210L190 174L115 210Z"
    fill="#6F9FD3"
/>

<path
    d="M265 194L335 132L405 170V190L335 153L265 211Z"
    fill="#79A8D9"
/>


<!-- FACTORY WINDOWS -->

<g fill="#DCEBFA">

    <rect x="137" y="222" width="42" height="38" rx="3"/>

    <rect x="194" y="222" width="42" height="38" rx="3"/>

    <rect x="285" y="214" width="42" height="38" rx="3"/>

    <rect x="342" y="214" width="42" height="38" rx="3"/>

</g>


<!-- FACTORY DOORS -->

<g fill="#416F9F">

    <rect x="218" y="264" width="48" height="36" rx="3"/>

    <rect x="288" y="264" width="48" height="36" rx="3"/>

</g>


<!-- CHIMNEYS -->

<rect
    x="166"
    y="82"
    width="28"
    height="94"
    rx="3"
    fill="#83A9D4"
/>

<rect
    x="161"
    y="78"
    width="38"
    height="10"
    rx="2"
    fill="#6D98C9"
/>


<rect
    x="350"
    y="56"
    width="31"
    height="94"
    rx="3"
    fill="#729BCB"
/>

<rect
    x="345"
    y="52"
    width="41"
    height="10"
    rx="2"
    fill="#5E8FC6"
/>


<!-- SMOKE -->

<path
    d="M174 72c-12-12 10-18 0-31M183 68c-7-12 12-18 4-30M359 43c-10-12 11-17 2-28"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="7"
    stroke-linecap="round"
    opacity=".45"
/>


<!-- WAREHOUSE -->

<path
    d="M430 300V220L505 183L580 220V300Z"
    fill="#9BBDE2"
/>

<path
    d="M430 220L505 183L580 220V234L505 198L430 234Z"
    fill="#7FA9D6"
/>


<!-- WAREHOUSE DOORS -->

<rect
    x="452"
    y="244"
    width="40"
    height="56"
    rx="3"
    fill="#4F7EAE"
/>

<rect
    x="513"
    y="244"
    width="43"
    height="56"
    rx="3"
    fill="#4F7EAE"
/>


<!-- INDUSTRIAL TANKS -->

<g fill="#82A9D4">

    <rect
        x="604"
        y="202"
        width="48"
        height="98"
        rx="17"
    />

    <rect
        x="665"
        y="226"
        width="39"
        height="74"
        rx="15"
    />

</g>


<g fill="#A8C7E8">

    <ellipse
        cx="628"
        cy="204"
        rx="24"
        ry="9"
    />

    <ellipse
        cx="684.5"
        cy="228"
        rx="19.5"
        ry="8"
    />

</g>


<!-- CONVEYOR BELT -->

<path
    d="M0 330H760"
    stroke="#5F91C6"
    stroke-width="13"
    stroke-linecap="round"
    opacity=".65"
/>

<path
    d="M0 344H760"
    stroke="#DCEBFA"
    stroke-width="3"
/>


<!-- CONVEYOR ROLLERS -->

<g fill="#5B83B0">

    <circle cx="55" cy="337" r="5"/>

    <circle cx="130" cy="337" r="5"/>

    <circle cx="205" cy="337" r="5"/>

    <circle cx="280" cy="337" r="5"/>

    <circle cx="355" cy="337" r="5"/>

    <circle cx="430" cy="337" r="5"/>

    <circle cx="505" cy="337" r="5"/>

    <circle cx="580" cy="337" r="5"/>

    <circle cx="655" cy="337" r="5"/>

    <circle cx="730" cy="337" r="5"/>

</g>


<!-- MOVING BOXES -->

<g>

    <rect
        x="75"
        y="302"
        width="42"
        height="27"
        rx="3"
        fill="#D6E7FA"
    />

    <path
        d="M75 311H117"
        stroke="#8CB1DB"
        stroke-width="3"
    />

    <rect
        x="395"
        y="302"
        width="42"
        height="27"
        rx="3"
        fill="#C5DDF6"
    />

    <path
        d="M395 311H437"
        stroke="#8CB1DB"
        stroke-width="3"
    />

</g>


<!-- MACHINE SENSOR INDICATORS -->

<g>

    <circle
        cx="335"
        cy="264"
        r="12"
        fill="#FFFFFF"
        opacity=".45"
    />

    <circle
        cx="335"
        cy="264"
        r="5"
        fill="#2877D5"
    />


    <circle
        cx="505"
        cy="236"
        r="12"
        fill="#FFFFFF"
        opacity=".45"
    />

    <circle
        cx="505"
        cy="236"
        r="5"
        fill="#2877D5"
    />


    <circle
        cx="628"
        cy="238"
        r="12"
        fill="#FFFFFF"
        opacity=".45"
    />

    <circle
        cx="628"
        cy="238"
        r="5"
        fill="#2877D5"
    />

</g>

</svg>
"""
