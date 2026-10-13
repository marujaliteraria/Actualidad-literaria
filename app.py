# --- SECCIÓN 3: TOP 10 Y RED NEURONAL / MAPA DE RELACIONES ---
st.markdown("---")
st.subheader("🌐 Cartografía de Relaciones y Tendencias del Corpus")

# Dividimos la sección en dos columnas (Izquierda: Top 10 | Derecha: Red Neuronal)
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
  st.markdown("### 🏆 Top Temas y Autores")
  st.markdown(
    "_Los ejes temáticos y figuras más recurrentes en el corpus analizado._"
  )

  # Contar frecuencia de temas/autores
  conteo_temas = {}
  for item in corpus_literario:
    t = item["tema"]
    conteo_temas[t] = conteo_temas.get(t, 0) + 1

  # Ordenar de mayor a menor y tomar los primeros 10
  temas_ordenados = sorted(
      conteo_temas.items(), key=lambda x: x[1], reverse=True
  )[:10]

  # Mostrar como una lista ordenada bonita con barrita visual simulada
  for i, (tema, cantidad) in enumerate(temas_ordenados, 1):
    st.markdown(f"**{i}. {tema}** — `({cantidad} menciones)`")

with col_der:
  st.markdown("### 🧠 Red Neuronal / Mapa del Campo Literario")
  st.markdown("_Visualización de conexiones entre contenidos y palabras clave._")

  # Intentamos importar la librería de grafos interactivos
  try:
    from streamlit_agraph import Agraph, Edge, Node, Config

    # Construimos los nodos y conexiones (grafo)
    nodes = []
    edges = []

    # Para evitar duplicados de nodos
    nodos_agregados = set()

    for item in corpus_literario:
      # Nodo principal (el contenido / creador)
      id_creador = item["nombre"]
      if id_creador not in nodos_agregados:
        nodes.append(
            Node(
                id=id_creador,
                label=id_creador,
                size=20,
                color="#0369a1",
                shape="dot",
            )
        )
        nodos_agregados.add(id_creador)

      # Nodos de palabras clave y conexiones
      for palabra in item["palabras_clave"]:
        id_palabra = f"#{palabra}"
        if id_palabra not in nodos_agregados:
          nodes.append(
              Node(
                  id=id_palabra,
                  label=id_palabra,
                  size=15,
                  color="#10b981",
                  shape="box",
              )
          )
          nodos_agregados.add(id_palabra)

        # Conectar el creador con su palabra clave (la "sinapsis" de la red)
        edges.append(
            Edge(
                source=id_creador,
                target=id_palabra,
                color="#cbd5e1",
                width=1.5,
            )
        )

    # Configuración visual del grafo estilo red neuronal / constelación
    config = Config(
        width=500,
        height=400,
        directed=False,
        nodeHighlightBehavior=True,
        highlightColor="#f59e0b",
        collapsible=False,
        physics={
            "barnesHut": {
                "gravitationalConstant": -2000,
                "centralGravity": 0.3,
                "springLength": 90,
            }
        },
    )

    # Renderizar el grafo interactivo en Streamlit
    Agraph(nodes=nodes, edges=edges, config=config)

  except ImportError:
    # Plan B por si no está instalada la librería de grafos en el entorno
    st.warning(
        "Para ver el mapa interactivo de red, asegurate de instalar la librería"
        " `streamlit-agraph` en tu proyecto."
    )
    # Mostramos un resumen textual de relaciones cruzadas como alternativa
    st.markdown(
        "**Conexiones detectadas en el corpus:**\n- Los contenidos se"
        " interconectan a través de etiquetas compartidas como *terror*,"
        " *atmósfera* y *canon argentino*."
    )
    # --- SECCIÓN 3: TOP 10 Y MAPA DE RED / CONEXIONES DEL CORPUS ---
st.markdown("---")
st.subheader("🌐 Cartografía de Relaciones y Tendencias del Corpus")

col_izq, col_der = st.columns(1)  # Lo adaptamos en una vista limpia o dos columnas

col_i, col_d = st.columns(2)

with col_i:
  st.markdown("### 🏆 Top Temas y Autores")
  st.markdown(
    "_Los ejes temáticos y figuras más recurrentes en el corpus analizado._"
  )

  conteo_temas = {}
  for item in corpus_literario:
    t = item["tema"]
    conteo_temas[t] = conteo_temas.get(t, 0) + 1

  temas_ordenados = sorted(
      conteo_temas.items(), key=lambda x: x[1], reverse=True
  )[:10]

  for i, (tema, cantidad) in enumerate(temas_ordenados, 1):
    st.markdown(f"**{i}. {tema}** — `({cantidad} menciones)`")

with col_d:
  st.markdown("### 🧠 Mapa de Red Discursiva")
  st.markdown("_Conexiones cruzadas entre conceptos clave del campo._")

  # Creamos una simulación visual de red por etiquetas compartidas
  st.info(
      "💡 **Nodo Central Activo:** El campo se articula en torno a tres"
      " grandes constelaciones de sentido:"
  )

  st.markdown(
      """
    - 🔴 **Eje Terror / Conurbano:** Vincula a *Mariana Enríquez* con *Samanta Schweblin* a través de etiquetas como `#siniestro`, `#atmósfera` y `#distopía`.
    - 🔵 **Eje Canon / Memoria:** Conecta a *Fogwill* con los debates sobre la dictadura y el `#humor_negro`.
    - 🟢 **Eje Crítica Contemporánea:** Agrupa las discusiones sobre la legibilidad de los clásicos (ej. *James Joyce*) en plataformas digitales.
    """
  )

  # Selector interactivo para "navegar" la red de forma textual
  palabra_a_explorar = st.selectbox(
      "Seleccioná una etiqueta para ver su red de nodos:",
      ["#terror", "#canon_argentino", "#atmósfera", "#ficción"],
  )

  # Mostrar qué elementos del corpus conectan con esa etiqueta
  relacionados_red = [
      item
      for item in corpus_literario
      if any(
          palabra_a_explorar.replace("#", "") in p.lower()
          for p in item["palabras_clave"]
      )
  ]

  if relacionados_red:
    st.markdown(
        f"**Contenidos vinculados a `{palabra_a_explorar}`:**"
    )
    for rel in relacionados_red:
      st.markdown(
          f"- 🔗 **{rel['nombre']}** ({rel['canal']}): _{rel['tema']}_"
      )
  else:
    st.markdown("_No hay conexiones directas en esta muestra._")
