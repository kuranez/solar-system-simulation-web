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
	<div id="wrapper" style="position: relative; width: 100%; height: 100%; overflow: hidden; background: transparent;">
	  <canvas id="trail_canvas" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block;"></canvas>
	  <canvas id="hud_canvas" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block; pointer-events: none;"></canvas>
	</div>
	"""

	_scripts = {
		"frame_data": """
		const payload = data.frame_data || {}
		if (!payload.bodies) {
		  return
		}

		const ratio = window.devicePixelRatio || 1
		const rect = wrapper.getBoundingClientRect()
		const cssWidth = Math.max(1, Math.round(rect.width || payload.canvas_width || model.width || 1))
		const cssHeight = Math.max(1, Math.round(rect.height || payload.canvas_height || model.height || 1))
		const pixelWidth = Math.max(1, Math.round(cssWidth * ratio))
		const pixelHeight = Math.max(1, Math.round(cssHeight * ratio))
		const canvasState = state
		const sceneId = payload.scene_id || ''
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
		trail_canvas.getContext('2d').setTransform(ratio, 0, 0, ratio, 0, 0)
		hud_canvas.getContext('2d').setTransform(ratio, 0, 0, ratio, 0, 0)

		const trailCtx = trail_canvas.getContext('2d')
		const hudCtx = hud_canvas.getContext('2d')
		const bg = Array.isArray(payload.background) ? payload.background : [6, 11, 21]
		const bgColor = `rgb(${bg[0]}, ${bg[1]}, ${bg[2]})`
		const textColor = payload.text_color ? `rgb(${payload.text_color[0]}, ${payload.text_color[1]}, ${payload.text_color[2]})` : 'rgb(230, 181, 110)'
		const trailFadeAlpha = typeof payload.trail_fade_alpha === 'number' ? payload.trail_fade_alpha : 0.08

		if (resized || sceneChanged || payload.reset) {
		  canvasState.trails = {}
		  canvasState.sceneId = sceneId
		  trailCtx.clearRect(0, 0, cssWidth, cssHeight)
		  trailCtx.fillStyle = bgColor
		  trailCtx.fillRect(0, 0, cssWidth, cssHeight)
		} else {
		  trailCtx.save()
		  trailCtx.globalAlpha = Math.max(0.01, Math.min(0.2, trailFadeAlpha))
		  trailCtx.fillStyle = bgColor
		  trailCtx.fillRect(0, 0, cssWidth, cssHeight)
		  trailCtx.restore()
		}

		hudCtx.clearRect(0, 0, cssWidth, cssHeight)
		hudCtx.fillStyle = textColor
		hudCtx.strokeStyle = 'rgba(255, 214, 150, 0.85)'
		hudCtx.lineJoin = 'round'
		hudCtx.lineCap = 'round'
		canvasState.trails = canvasState.trails || {}

		const maxTrailPoints = payload.max_trail_points || 1800
		for (const body of payload.bodies) {
		  const point = {x: body.x, y: body.y}
		  const bodyKey = body.name || `${point.x}:${point.y}`
		  const previous = canvasState.trails[bodyKey]
		  if (body.draw_line !== false && previous) {
		    trailCtx.beginPath()
		    trailCtx.moveTo(previous.x, previous.y)
		    trailCtx.lineTo(point.x, point.y)
		    trailCtx.strokeStyle = `rgba(${body.color[0]}, ${body.color[1]}, ${body.color[2]}, 0.72)`
		    trailCtx.lineWidth = Math.max(1, Math.min(3, (body.radius || 1) * 0.12))
		    trailCtx.stroke()
		  }
		  canvasState.trails[bodyKey] = point
		  const trailKeys = Object.keys(canvasState.trails)
		  if (trailKeys.length > maxTrailPoints) {
		    delete canvasState.trails[trailKeys[0]]
		  }
		}

		for (const body of payload.bodies) {
		  const x = body.x
		  const y = body.y
		  const radius = Math.max(1, Math.round(body.radius || 1))
		  const color = `rgb(${body.color[0]}, ${body.color[1]}, ${body.color[2]})`

		  hudCtx.beginPath()
		  hudCtx.arc(x, y, radius, 0, Math.PI * 2)
		  hudCtx.fillStyle = color
		  hudCtx.fill()
		}

		hudCtx.font = '16px monospace'
		hudCtx.fillStyle = textColor
		let textY = 22
		if (payload.time_text) {
		  hudCtx.fillText(payload.time_text, 12, textY)
		  textY += 20
		}
		if (payload.scale_text) {
		  hudCtx.fillText(payload.scale_text, 12, textY)
		  textY += 20
		}
		if (Array.isArray(payload.notifications)) {
		  hudCtx.textAlign = 'right'
		  let noteY = 22
		  for (const note of payload.notifications) {
		    hudCtx.fillText(note, cssWidth - 12, noteY)
		    noteY += 20
		  }
		  hudCtx.textAlign = 'left'
		}

		if (Array.isArray(payload.hud_rows)) {
		  for (const row of payload.hud_rows) {
		    const rowColor = Array.isArray(row.color) ? `rgb(${row.color[0]}, ${row.color[1]}, ${row.color[2]})` : textColor
		    hudCtx.fillStyle = rowColor
		    hudCtx.fillText(row.text, 12 + (row.indent || 0), textY)
		    textY += 20
		  }
		}
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
			return text
		text = f"{prefix}{body.name}: {_distance_label(body, parent)}"
		if hasattr(body, "orbit_count"):
			text += f" | Orbits: {body.orbit_count}"
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
			"y": float(y),
			"radius": float(max(1, int(getattr(body, "radius", 1)))),
			"color": _rgb(getattr(body, "color", (0, 0, 0))),
			"draw_line": bool(getattr(body, "draw_line", True)),
			"flash": int(getattr(body, "orbit_complete_flash", 0)),
			"orbit_count": int(getattr(body, "orbit_count", 0)),
		}

	years = int(state.get("total_elapsed_time", 0.0) // (365.25 * 24 * 3600))
	remaining_time = state.get("total_elapsed_time", 0.0) % (365.25 * 24 * 3600)
	days = int(remaining_time // (24 * 3600))
	time_text = f"Time: {years}y {days}d" if years > 0 else f"Time: {days}d"
	meters_per_pixel = constants.AU / distance_scale if distance_scale else 0
	scale_text = f"Scale: {meters_per_pixel:.2e} m/px"

	notifications = [f"{body.name} completed an orbit" for body in bodies if getattr(body, "orbit_complete_flash", 0) > 0]

	return {
		"reset": bool(reset),
		"scene_id": int(scene_token),
		"background": _rgb(color_bg),
		"text_color": _rgb(constants.COLOR_TEXT),
		"canvas_width": canvas_width,
		"canvas_height": canvas_height,
		"distance_scale": distance_scale,
		"offset_x": offset_x,
		"offset_y": offset_y,
		"time_text": time_text,
		"scale_text": scale_text,
		"notifications": notifications,
		"max_trail_points": 1800,
		"trail_fade_alpha": 0.08,
		"hud_rows": _build_hud_rows(bodies),
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
