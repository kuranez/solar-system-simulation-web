"""Client-side canvas rendering for the solar system simulation."""

from __future__ import annotations

from collections import defaultdict

import panel as pn
import param

import constants


class SimulationCanvas(pn.reactive.ReactiveHTML):
	"""Browser-side canvas that renders a compact simulation frame payload."""

	frame_data = param.Dict(default={})

	_template = """
	<div id="wrapper" style="position: relative; width: 100%; height: 100%; overflow: hidden; background: transparent; touch-action: none; cursor: grab;">
	  <canvas id="trail_canvas" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block;"></canvas>
	  <canvas id="hud_canvas" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block; pointer-events: none;"></canvas>
	</div>
	"""

	_scripts = {
		"frame_data": """
		const payload = data.frame_data || {}
		const canvasState = state
		const ratio = window.devicePixelRatio || 1

		canvasState.viewZoom = typeof canvasState.viewZoom === 'number' ? canvasState.viewZoom : 1
		canvasState.viewPanX = typeof canvasState.viewPanX === 'number' ? canvasState.viewPanX : 0
		canvasState.viewPanY = typeof canvasState.viewPanY === 'number' ? canvasState.viewPanY : 0
		canvasState.trails = canvasState.trails || {}

		const clamp = (value, min, max) => Math.max(min, Math.min(max, value))
		const applyWorldTransform = (ctx) => {
		  ctx.setTransform(
		    ratio * canvasState.viewZoom,
		    0,
		    0,
		    ratio * canvasState.viewZoom,
		    ratio * canvasState.viewPanX,
		    ratio * canvasState.viewPanY,
		  )
		}
		const clearCanvas = (ctx, width, height) => {
		  ctx.setTransform(1, 0, 0, 1, 0, 0)
		  ctx.clearRect(0, 0, width, height)
		}
		const redraw = (nextPayload) => {
		  const activePayload = nextPayload || canvasState.lastPayload
		  if (!activePayload || !Array.isArray(activePayload.bodies)) {
		    return
		  }

		  canvasState.lastPayload = activePayload
		  const updateHistory = Boolean(nextPayload)
		  const rect = wrapper.getBoundingClientRect()
		  const cssWidth = Math.max(1, Math.round(rect.width || activePayload.canvas_width || model.width || 1))
		  const cssHeight = Math.max(1, Math.round(rect.height || activePayload.canvas_height || model.height || 1))
		  const pixelWidth = Math.max(1, Math.round(cssWidth * ratio))
		  const pixelHeight = Math.max(1, Math.round(cssHeight * ratio))
		  const sceneId = activePayload.scene_id || ''
		  const sceneChanged = canvasState.sceneId !== sceneId
		  const resized = trail_canvas.width !== pixelWidth || trail_canvas.height !== pixelHeight || hud_canvas.width !== pixelWidth || hud_canvas.height !== pixelHeight

		  if (resized) {
		    trail_canvas.width = pixelWidth
		    trail_canvas.height = pixelHeight
		    hud_canvas.width = pixelWidth
		    hud_canvas.height = pixelHeight
		  }

		  trail_canvas.style.width = cssWidth + 'px'
		  trail_canvas.style.height = cssHeight + 'px'
		  hud_canvas.style.width = cssWidth + 'px'
		  hud_canvas.style.height = cssHeight + 'px'

		  const trailCtx = trail_canvas.getContext('2d')
		  const hudCtx = hud_canvas.getContext('2d')
		  const bg = Array.isArray(activePayload.background) ? activePayload.background : [6, 11, 21]
		  const bgColor = `rgb(${bg[0]}, ${bg[1]}, ${bg[2]})`
		  const textColor = activePayload.text_color ? `rgb(${activePayload.text_color[0]}, ${activePayload.text_color[1]}, ${activePayload.text_color[2]})` : 'rgb(230, 181, 110)'
		  const trailFadeAlpha = typeof activePayload.trail_fade_alpha === 'number' ? activePayload.trail_fade_alpha : 0.028
		  const maxTrailPoints = activePayload.max_trail_points || 1800
		  const AU_METERS = 149597870700
		  const effectiveDistanceScale = (typeof activePayload.distance_scale === 'number' ? activePayload.distance_scale : 0) * canvasState.viewZoom
		  const metersPerPixel = effectiveDistanceScale ? 1.0 / effectiveDistanceScale : 0
		  const auPerPixel = metersPerPixel / AU_METERS
		  const scaleText = effectiveDistanceScale ? `Scale: ${metersPerPixel.toExponential(2)} m/px | ${auPerPixel.toExponential(2)} AU/px` : activePayload.scale_text

		  if (sceneChanged || activePayload.reset) {
		    canvasState.trails = {}
		    canvasState.sceneId = sceneId
		  }

		  clearCanvas(trailCtx, pixelWidth, pixelHeight)
		  trailCtx.fillStyle = bgColor
		  trailCtx.fillRect(0, 0, pixelWidth, pixelHeight)

		  clearCanvas(hudCtx, pixelWidth, pixelHeight)
		  trailCtx.save()
		  applyWorldTransform(trailCtx)
		  trailCtx.lineJoin = 'round'
		  trailCtx.lineCap = 'round'
		  const smoothstep = (edge0, edge1, value) => {
		    const t = clamp((value - edge0) / Math.max(1e-6, edge1 - edge0), 0, 1)
		    return t * t * (3 - (2 * t))
		  }

		  const drawTrailPoints = (points, alphaMultiplier, color, lineWidth, edgeFadeRatio, softenBothEnds) => {
		    if (!Array.isArray(points) || points.length < 2) {
		      return
		    }
		    const edgePoints = Math.max(1, Math.round(points.length * Math.max(0.02, edgeFadeRatio || 0.1)))
		    for (let i = 1; i < points.length; i += 1) {
		      const progress = i / Math.max(1, points.length - 1)
		      const fadeIn = smoothstep(0, edgePoints, i)
		      const fadeOut = softenBothEnds ? smoothstep(0, edgePoints, (points.length - 1) - i) : 1
		      const edgeWeight = softenBothEnds ? Math.min(fadeIn, fadeOut) : fadeIn
		      const alpha = clamp((trailFadeAlpha + (0.38 * Math.pow(progress, 1.12))) * alphaMultiplier * edgeWeight, 0.015, 0.72)
		      trailCtx.beginPath()
		      trailCtx.moveTo(points[i - 1].x, points[i - 1].y)
		      trailCtx.lineTo(points[i].x, points[i].y)
		      trailCtx.strokeStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`
		      trailCtx.lineWidth = lineWidth
		      trailCtx.stroke()
		    }
		  }

		  for (const body of activePayload.bodies) {
		    const point = { x: body.x, y: body.y }
		    const bodyKey = body.name || `${point.x}:${point.y}`
		    const currentOrbitCount = typeof body.orbit_count === 'number' ? body.orbit_count : 0
		    const storedTrailState = canvasState.trails[bodyKey]
		    const trailState = (storedTrailState && typeof storedTrailState === 'object' && !Array.isArray(storedTrailState)) ? storedTrailState : {
		      completed: [],
		      active: [],
		      lastOrbitCount: currentOrbitCount,
		    }
		    trailState.completed = Array.isArray(trailState.completed) ? trailState.completed : []
		    trailState.active = Array.isArray(trailState.active) ? trailState.active : []
		    trailState.lastOrbitCount = typeof trailState.lastOrbitCount === 'number' ? trailState.lastOrbitCount : currentOrbitCount
		    const currentColor = body.color || [200, 200, 200]
		    const currentLineWidth = Math.max(1, Math.min(3, (body.radius || 1) * 0.12))
		    const bodyCanDrawTrail = body.draw_line !== false

		    if (updateHistory) {
		      if (!bodyCanDrawTrail) {
		        trailState.completed = []
		        trailState.active = [point]
		        trailState.lastOrbitCount = currentOrbitCount
		      } else {
		        const last = trailState.active[trailState.active.length - 1]
		        const spacing = activePayload.trail_sample_spacing_px || 2.5
		        // Spatial sampling: Only store the point if the body moved significantly
		        const movedEnough = !last || (Math.pow(point.x - last.x, 2) + Math.pow(point.y - last.y, 2) > spacing * spacing)

		        if (currentOrbitCount > trailState.lastOrbitCount) {
		          trailState.completed = trailState.active.length > 1 ? trailState.active.slice() : []
		          trailState.active = []
		          trailState.lastOrbitCount = currentOrbitCount
		        }
		        if (movedEnough) {
		          trailState.active.push(point)
		          if (trailState.active.length > maxTrailPoints) {
		            trailState.active.shift()
		          }
		        }
		      }
		      canvasState.trails[bodyKey] = trailState
		    }

		    if (trailState.completed.length > 0) {
		      drawTrailPoints(trailState.completed, 0.78, [184, 184, 184], currentLineWidth, 0.24, true)
		    }
		    drawTrailPoints(trailState.active, 1.0, currentColor, currentLineWidth, 0.1, false)
		  }
		  trailCtx.restore()

		  hudCtx.save()
		  applyWorldTransform(hudCtx)
		  for (const body of activePayload.bodies) {
		    const radius = Math.max(1, Math.round(body.radius || 1))
		    const color = `rgb(${body.color[0]}, ${body.color[1]}, ${body.color[2]})`

		    hudCtx.beginPath()
		    hudCtx.arc(body.x, body.y, radius, 0, Math.PI * 2)
		    hudCtx.fillStyle = color
		    hudCtx.fill()
		  }
		  hudCtx.restore()

		  hudCtx.fillStyle = textColor
		  hudCtx.font = '16px monospace'
		  hudCtx.textAlign = 'left'
		  let textY = 22
		  if (activePayload.time_text) {
		    hudCtx.fillText(activePayload.time_text, 12, textY)
		    textY += 20
		  }
		  if (activePayload.speed_text) {
		    hudCtx.fillText(activePayload.speed_text, 12, textY)
		    textY += 20
		  }
		  if (scaleText) {
		    hudCtx.fillText(scaleText, 12, textY)
		    textY += 20
		  }
		  if (Array.isArray(activePayload.notifications)) {
		    hudCtx.textAlign = 'right'
		    let noteY = 22
		    for (const note of activePayload.notifications) {
		      hudCtx.fillText(note, cssWidth - 12, noteY)
		      noteY += 20
		    }
		    hudCtx.textAlign = 'left'
		  }

		  if (Array.isArray(activePayload.hud_rows)) {
		    for (const row of activePayload.hud_rows) {
		      const rowColor = Array.isArray(row.color) ? `rgb(${row.color[0]}, ${row.color[1]}, ${row.color[2]})` : textColor
		      hudCtx.fillStyle = rowColor
		      hudCtx.fillText(row.text, 12 + (row.indent || 0), textY)
		      textY += 20
		    }
		  }
		}

		if (!canvasState.listenersReady) {
		  canvasState.listenersReady = true
		  // Allow zooming much further out, but limit how far you can zoom in
		  const minZoom = 0.05
		  const maxZoom = 2.0
		  // Increase step so wheel scrolling feels responsive at wider ranges
		  const zoomStep = 0.0025

		  const finishDrag = () => {
		    canvasState.dragging = false
		    trail_canvas.style.cursor = 'grab'
		  }

		  const startDrag = (event) => {
		    if (event.button !== 0) {
		      return
		    }
		    canvasState.dragging = true
		    canvasState.lastPointerX = event.clientX
		    canvasState.lastPointerY = event.clientY
		    trail_canvas.style.cursor = 'grabbing'
		    if (trail_canvas.setPointerCapture) {
		      try {
		        trail_canvas.setPointerCapture(event.pointerId)
		      } catch (error) {
		        // Ignore pointer-capture failures in older browsers.
		      }
		    }
		    event.preventDefault()
		  }

		  const moveDrag = (event) => {
		    if (!canvasState.dragging) {
		      return
		    }
		    const dx = event.clientX - canvasState.lastPointerX
		    const dy = event.clientY - canvasState.lastPointerY
		    canvasState.viewPanX += dx
		    canvasState.viewPanY += dy
		    canvasState.lastPointerX = event.clientX
		    canvasState.lastPointerY = event.clientY
		    redraw()
		    event.preventDefault()
		  }

		  const zoomAtPointer = (event) => {
		    if (!canvasState.lastPayload || !Array.isArray(canvasState.lastPayload.bodies)) {
		      return
		    }
		    const rect = wrapper.getBoundingClientRect()
		    const cursorX = event.clientX - rect.left
		    const cursorY = event.clientY - rect.top
		    const oldZoom = canvasState.viewZoom || 1
		    const zoomFactor = Math.exp(-event.deltaY * zoomStep)
		    const newZoom = clamp(oldZoom * zoomFactor, minZoom, maxZoom)
		    if (newZoom === oldZoom) {
		      return
		    }
		    const worldX = (cursorX - canvasState.viewPanX) / oldZoom
		    const worldY = (cursorY - canvasState.viewPanY) / oldZoom
		    canvasState.viewPanX = cursorX - (worldX * newZoom)
		    canvasState.viewPanY = cursorY - (worldY * newZoom)
		    canvasState.viewZoom = newZoom
		    redraw()
		    event.preventDefault()
		  }

		  trail_canvas.addEventListener('pointerdown', startDrag)
		  trail_canvas.addEventListener('pointermove', moveDrag)
		  trail_canvas.addEventListener('pointerup', finishDrag)
		  trail_canvas.addEventListener('pointercancel', finishDrag)
		  trail_canvas.addEventListener('pointerleave', finishDrag)
		  trail_canvas.addEventListener('wheel', zoomAtPointer, { passive: false })
		}

		redraw(payload)
		""",
	}


def _rgb(value, default=(0, 0, 0)):
	if isinstance(value, (list, tuple)) and len(value) >= 3:
		return [int(value[0]), int(value[1]), int(value[2])]
	return [int(default[0]), int(default[1]), int(default[2])]


def _parent_of(body):
	return getattr(body, "parent_body", None) or getattr(body, "child_of", None)


def _distance_between(body_a, body_b):
	if body_a is None or body_b is None:
		return 0.0
	return (((body_a.x - body_b.x) ** 2 + (body_a.y - body_b.y) ** 2) ** 0.5)


def _body_children_map(bodies):
	children_map = defaultdict(list)
	seen_children = defaultdict(set)

	for body in bodies:
		for child in getattr(body, "children", []) or []:
			if child is None or child in seen_children[body]:
				continue
			children_map[body].append(child)
			seen_children[body].add(child)

	for body in bodies:
		parent = _parent_of(body)
		if parent is not None and body not in seen_children[parent]:
			children_map[parent].append(body)
			seen_children[parent].add(body)

	return children_map


def _build_hud_rows(bodies):
	children_map = _body_children_map(bodies)
	sun = next((body for body in bodies if getattr(body, "is_sun", False)), None)
	rows = []
	visited = set()

	def _distance_label(body, parent):
		if parent is None:
			return "stationary"

		distance = _distance_between(body, parent)
		if getattr(parent, "is_sun", False):
			return f"{distance / 1000:,.0f} km ({distance / constants.AU:.2f} AU)"

		return f"{distance / 1000:,.0f} km from {parent.name}"

	def _orbit_minmax_rows(body, parent):
		if getattr(body, "static_body", False):
			return []

		measured_min = getattr(body, "orbit_min_distance", None)
		measured_max = getattr(body, "orbit_max_distance", None)
		measured_mean = getattr(body, "orbit_delta_mean", None)
		ref_min = getattr(body, "perihelion", None) or getattr(body, "perigee", None) or getattr(body, "average_distance", None)
		ref_max = getattr(body, "aphelion", None) or getattr(body, "apogee", None) or getattr(body, "average_distance", None)
		if ref_min is None and ref_max is None and measured_min is None and measured_max is None:
			return []

		rows = []
		if ref_min is not None:
			parts = []
			if getattr(parent, "is_sun", False):
				parts.append(f"min: {ref_min/1000:,.0f} km ({ref_min/constants.AU:.2f} AU)")
			else:
				parts.append(f"min: {ref_min/1000:,.0f} km")
			if measured_min is not None and ref_min:
				delta_min = ((measured_min - ref_min) / ref_min) * 100.0
				parts.append(f"Δmin: {delta_min:+.2f}%")
			if measured_mean is not None and ref_min:
				parts.append(f"Δmean: {(measured_mean / ref_min) * 100.0:.2f}%")
			rows.append(" | ".join(parts))
		if ref_max is not None:
			parts = []
			if getattr(parent, "is_sun", False):
				parts.append(f"max: {ref_max/1000:,.0f} km ({ref_max/constants.AU:.2f} AU)")
			else:
				parts.append(f"max: {ref_max/1000:,.0f} km")
			if measured_max is not None and ref_max:
				delta_max = ((measured_max - ref_max) / ref_max) * 100.0
				parts.append(f"Δmax: {delta_max:+.2f}%")
			if measured_mean is not None and ref_max:
				parts.append(f"Δmean: {(measured_mean / ref_max) * 100.0:.2f}%")
			rows.append(" | ".join(parts))

		return rows

	def _row_text(body, parent, depth):
		prefix = "- " if depth > 0 else ""
		if getattr(body, "static_body", False):
			return f"{prefix}{body.name}: stationary"
		if parent is None:
			if getattr(body, "is_sun", False):
				return f"{body.name}: stationary"
			distance = _distance_between(body, sun) if sun is not None else getattr(body, "distance_to_sun", 0.0)
			text = f"{body.name}: {distance / 1000:,.0f} km ({distance / constants.AU:.2f} AU)"
			if hasattr(body, "orbit_count"):
				text += f" | Orbits: {body.orbit_count}"
			# Append min/max distances when available (skip stationary bodies)
			if not getattr(body, "static_body", False):
				# Prefer instance attributes, fall back to constants lookup by name
				min_d = getattr(body, "perihelion", None) or getattr(body, "perigee", None) or getattr(body, "average_distance", None)
				max_d = getattr(body, "aphelion", None) or getattr(body, "apogee", None) or getattr(body, "average_distance", None)
				if min_d is None or max_d is None:
					const_entry = None
					try:
						const_entry = constants.BODIES_DATA.get(getattr(body, "name", ""), None) or (constants.MOON_DATA if getattr(body, "name", "") == "Moon" else None)
					except Exception:
						const_entry = None
					if const_entry:
						if min_d is None:
							min_d = const_entry.get("perihelion") or const_entry.get("perigee") or const_entry.get("average_distance")
						if max_d is None:
							max_d = const_entry.get("aphelion") or const_entry.get("apogee") or const_entry.get("average_distance")
				parts = []
				if min_d is not None:
					if getattr(parent, "is_sun", False):
						parts.append(f"min: {min_d/1000:,.0f} km ({min_d/constants.AU:.2f} AU)")
					else:
						parts.append(f"min: {min_d/1000:,.0f} km")
				if max_d is not None:
					if getattr(parent, "is_sun", False):
						parts.append(f"max: {max_d/1000:,.0f} km ({max_d/constants.AU:.2f} AU)")
					else:
						parts.append(f"max: {max_d/1000:,.0f} km")
				if parts:
					# moved to subrow; do not append inline
					pass
				return text
		text = f"{prefix}{body.name}: {_distance_label(body, parent)}"
		if hasattr(body, "orbit_count"):
			text += f" | Orbits: {body.orbit_count}"
		# Append min/max distances when available for non-stationary bodies
		if not getattr(body, "static_body", False):
			min_d = getattr(body, "perihelion", None) or getattr(body, "perigee", None) or getattr(body, "average_distance", None)
			max_d = getattr(body, "aphelion", None) or getattr(body, "apogee", None) or getattr(body, "average_distance", None)
			if min_d is None or max_d is None:
				const_entry = None
				try:
					const_entry = constants.BODIES_DATA.get(getattr(body, "name", ""), None) or (constants.MOON_DATA if getattr(body, "name", "") == "Moon" else None)
				except Exception:
					const_entry = None
				if const_entry:
					if min_d is None:
						min_d = const_entry.get("perihelion") or const_entry.get("perigee") or const_entry.get("average_distance")
					if max_d is None:
						max_d = const_entry.get("aphelion") or const_entry.get("apogee") or const_entry.get("average_distance")
			parts = []
			if min_d is not None:
				if getattr(parent, "is_sun", False):
					parts.append(f"min: {min_d/1000:,.0f} km ({min_d/constants.AU:.2f} AU)")
				else:
					parts.append(f"min: {min_d/1000:,.0f} km")
			if max_d is not None:
				if getattr(parent, "is_sun", False):
					parts.append(f"max: {max_d/1000:,.0f} km ({max_d/constants.AU:.2f} AU)")
				else:
					parts.append(f"max: {max_d/1000:,.0f} km")
			if parts:
				# moved to subrow; do not append inline
				pass
		return text

	def _walk(body, parent, depth):
		if body in visited:
			return
		visited.add(body)
		rows.append({
			"text": _row_text(body, parent, depth),
			"indent": 10 + (depth * 20),
			"color": _rgb(getattr(body, "color", constants.COLOR_TEXT), constants.COLOR_TEXT),
		})
		# add measured orbit extrema as a subrow if available (skip stationary bodies)
		for minmax_row in _orbit_minmax_rows(body, parent):
			rows.append({
				"text": minmax_row,
				"indent": 10 + ((depth + 1) * 20),
				"color": _rgb(getattr(constants, "COLOR_HUD_TEXT", constants.COLOR_TEXT)),
			})
		for child in children_map.get(body, []):
			_walk(child, body, depth + 1)

	for root in [body for body in bodies if _parent_of(body) is None]:
		_walk(root, None, 0)

	return rows



def build_frame_data(bodies, state, color_bg, *, scene_token, reset=False):
	"""Create the compact browser-canvas payload for one simulation frame."""
	distance_scale = state["distance_scale"]
	offset_x = state["offset_x"]
	offset_y = state["offset_y"]
	canvas_width = constants.WIDTH
	canvas_height = constants.HEIGHT

	def _screen_position(body):
		return body._screen_position(distance_scale, offset_x, offset_y)

	def _body_payload(body):
		x, y = _screen_position(body)
		return {
			"name": getattr(body, "name", "Body"),
			"x": float(x),
			"y": round(float(y), 1),
			"radius": float(max(1, int(getattr(body, "radius", 1)))),
			"color": _rgb(getattr(body, "color", (0, 0, 0))),
			"draw_line": bool(getattr(body, "draw_line", True)),
			"orbit_count": int(getattr(body, "orbit_count", 0)),
		}

	years = int(state.get("total_elapsed_time", 0.0) // (365.25 * 24 * 3600))
	remaining_time = state.get("total_elapsed_time", 0.0) % (365.25 * 24 * 3600)
	days = int(remaining_time // (24 * 3600))
	time_text = f"Time: {years}y {days}d" if years > 0 else f"Time: {days}d"
	meters_per_pixel = 1.0 / distance_scale if distance_scale else 0
	au_per_pixel = meters_per_pixel / constants.AU if distance_scale else 0
	scale_text = f"Scale: {meters_per_pixel:.2e} m/px | {au_per_pixel:.2e} AU/px"
	frame_period = int(state.get("frame_period", 80))
	simulation_timestep = float(state.get("simulation_timestep", constants.TIMESTEP))
	render_stride = float(state.get("render_stride", 1.0))
	if render_stride > 1:
		speed_text = f"Step: {simulation_timestep / 86400.0:.1f} d/frame | Render x{render_stride:g}"
	else:
		speed_text = f"Step: {simulation_timestep / 86400.0:.1f} d/frame"

	# Throttle HUD row generation to reduce object churn
	hud_counter = state.get("_hud_counter", 0)
	if reset or hud_counter <= 0:
		hud_rows = _build_hud_rows(bodies)
		state["_hud_cache"] = hud_rows
		state["_hud_counter"] = 10  # Update HUD every 10 frames
	else:
		hud_rows = state.get("_hud_cache", [])
		state["_hud_counter"] = hud_counter - 1

	return {
		"reset": bool(reset),
		"scene_id": int(scene_token),
		"background": _rgb(color_bg),
		"text_color": _rgb(constants.COLOR_TEXT),
		"canvas_width": canvas_width,
		"canvas_height": canvas_height,
		"distance_scale": distance_scale,
		"simulation_timestep": simulation_timestep,
		"offset_x": offset_x,
		"offset_y": offset_y,
		"time_text": time_text,
		"speed_text": speed_text,
		"scale_text": scale_text,
        
		"max_trail_points": 1800,
		"max_completed_orbit_trails": int(state.get("max_completed_orbit_trails", 3)),
		"min_orbits_before_prune": int(state.get("min_orbits_before_prune", 1)),
		"trail_sample_spacing_px": float(state.get("trail_sample_spacing_px", 2.5)),
		"trail_fade_alpha": 0.028,
		"hud_rows": hud_rows,
		"bodies": [_body_payload(body) for body in bodies],
	}



def sync_canvas_frame(canvas_view, bodies, state, color_bg, *, scene_token, reset=False):
	"""Push the current frame state to a SimulationCanvas component."""
	canvas_view.frame_data = build_frame_data(
		bodies,
		state,
		color_bg,
		scene_token=scene_token,
		reset=reset,
	)
