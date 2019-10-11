import socket
import struct


BROADCAST_PORT = 9090
TCP_PORT = 7788
PREAMBLE = 'Logitech control'

COMMAND_THROTTLE = 0
COMMAND_STEERING = 1


class LogitechSteeringWheelController(object):
    def __init__(self, *args, **kwargs):
        bc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        bc_sock.bind(('', BROADCAST_PORT))

        last_str = ''
        print('Matching ...')
        while True:
            this_str, addr = bc_sock.recvfrom(1024)
            this_str = this_str.decode()
            if PREAMBLE in last_str + this_str:
                self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_sock.connect((addr[0], TCP_PORT))
                break
            last_str = this_str

        print('Matched  {} {}'.format(addr[0], addr[1]))
        self.new_throttle = 0
        self.new_steering = 0
        self.throttle_scale = kwargs['throttle_scale']
        self.steering_scale = kwargs['steering_scale']

    def update(self):
        buffer = b''
        while True:
            data = self.tcp_sock.recv(4096)
            buffer += data
            while len(buffer) >= 8:
                cmd, val = struct.unpack('>Ii', buffer[:8])
                buffer = buffer[8:]

                if cmd == COMMAND_THROTTLE:
                    self.new_throttle = val / 32767 * self.throttle_scale
                elif cmd == COMMAND_STEERING:
                    self.new_steering = val / 32767 * self.steering_scale
                # print(self.new_throttle, self.new_steering)

    def run_threaded(self, img_arr=None):
        return self.new_steering, self.new_throttle, 'user', False

    def set_deadzone(self, val):
        self.dead_zone = val


if __name__ == '__main__':
    ctrl = LogitechSteeringWheelController()
