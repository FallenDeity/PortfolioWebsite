from __future__ import annotations

import fastapi

from . import Extension, route


class Profile(Extension):
    @route(path="/blog", response_model=fastapi.responses.HTMLResponse)
    async def blog(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = self.app.get_image("footers")
        gist = self.app.github.get_gist("426ec7974f705303a2363c739dd82309")
        file = gist.files[list(gist.files.keys())[0]]
        name = file.filename.split(".")[0].replace("-", " ").title()
        content = self.app.github.render_markdown(file.content.replace("user-content-", ""))
        return self.app.templates.TemplateResponse(
            "blog_template.html",
            {
                "request": request,
                "title": "Blog",
                "f_img": f_img,
                "name": name,
                "content": content,
            },
        )
