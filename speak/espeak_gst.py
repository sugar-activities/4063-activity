# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
logger = logging.getLogger('speak')

from gi.repository import Gst
import espeak

PITCH_MAX = 200
RATE_MAX = 200
PITCH_DEFAULT = PITCH_MAX/2
RATE_DEFAULT = RATE_MAX/2

class AudioGrabGst(espeak.BaseAudioGrab):
    def speak(self, status, text):
        self.make_pipeline('espeak name=espeak ! autoaudiosink')
        src = self.pipeline.get_by_name('espeak')

        pitch = int(status.pitch) - 100
        rate = int(status.rate) - 100

        logger.debug('pitch=%d rate=%d voice=%s text=%s' % (pitch, rate,
                status.voice.name, text))

        src.props.text = text
        src.props.pitch = pitch
        src.props.rate = rate
        src.props.voice = status.voice.name

        self.restart_sound_device()

def voices():
    out = []

    for i in Gst.ElementFactory.make('espeak', None).props.voices:
        name, language, dialect = i
        if name in ('en-rhotic','english_rp','english_wmids'):
            # these voices don't produce sound
            continue
        out.append((language, name, dialect))

    return out
