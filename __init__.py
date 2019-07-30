# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.
from flask import Flask, request, render_template

user = 'admin'
pwd = 'Start!123'
app = Flask(__name__)
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import webbrowser

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class TemplateSkill(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(TemplateSkill, self).__init__(name="TemplateSkill")

        # Initialize working variables used within the skill.
        self.count = 0

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Server").require("Server").require("Server"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if message.data["Server"] == "stop":
            webbrowser.open('http://localhost/index.php')
            self.speak_dialog("web.server.shutdown")
        if message.data["Server"] == "restart":
            webbrowser.open('http://example.com')
        if message.data["Server"] == "start":
            self.speak_dialog("web.server.start")

    @intent_handler(IntentBuilder("").require("Count").require("Dir"))
    def handle_count_intent(self, message):
        if message.data["Dir"] == "up":
            self.count += 1
        else:  # assume "down"
            self.count -= 1
        self.speak_dialog("count.is.now", data={"count": self.count})
    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return TemplateSkill()
    
@app.route("/", methods=['GET','POST'])
def index():
	return "Welcome to the flask world!"

@app.route("/shutdown", methods = ['POST'])
def shutdown_server():
	print("Shutdown context hit with POST!")
	if request.form.get('username') and request.form.get('password'):
		print('Got username: {} and password: {}'.format(request.form.get('username'),request.form.get('password')))
		if request.form.get('username') != user:
			return 'The username or password is incorrect!'

		if request.form.get('password') != pwd:
			return 'The username or password is incorrect!'

		print("It seems to be valid, the server is shutting down!")
		shutdown = request.environ.get('werkzeug.server.shutdown')
		if shutdown is None:
			raise RuntimeError('The function is unavailable!')
		else:
			shutdown()
			return "THe server is shutting down!"

	else:
		return 'You need authorization to shut the server down!'


if __name__ == '__main__':
    app.run(port = 8081, host = '0.0.0.0', debug = True)