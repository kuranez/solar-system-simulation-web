"""Moon implementation for the new object model."""


from .base import Body


class Moon(Body):
	def __init__(self, x, y, radius, mass, name="Moon", color=(200, 200, 200), parent_body=None, x_vel=0.0, y_vel=0.0):
		"""Moon is a Body that can be registered as a child of another Body.

		Arguments:
		- parent_body: legacy kw accepting the parent Body (kept for compatibility)
		- child relationship is stored in `child_of` and the parent will have this moon in its `children` list.
		"""
		super().__init__(x, y, radius, mass, name=name, color=color)
		# canonical parent reference
		self.child_of = parent_body
		# keep legacy attribute for code expecting `parent_body`
		self.parent_body = parent_body
		self.x_vel = x_vel
		self.y_vel = y_vel

		# auto-register on parent's children list (avoid duplicates)
		if parent_body is not None:
			try:
				if not hasattr(parent_body, 'children'):
					parent_body.children = []
				if self not in parent_body.children:
					parent_body.children.append(self)
			except Exception:
				# don't let child registration break initialization
				pass
