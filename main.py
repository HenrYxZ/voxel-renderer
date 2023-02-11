import pyglet


from app import App


app = App()


if __name__ == '__main__':
    pyglet.clock.schedule(app.on_update)
    pyglet.app.run()
