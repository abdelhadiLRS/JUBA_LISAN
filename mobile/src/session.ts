import AsyncStorage from '@react-native-async-storage/async-storage'

const GUEST_KEY = 'juba_lisan_guest_mode'

export async function isGuestMode(): Promise<boolean> {
  return (await AsyncStorage.getItem(GUEST_KEY)) === '1'
}

export async function enterGuestMode() {
  await AsyncStorage.setItem(GUEST_KEY, '1')
}

export async function leaveGuestMode() {
  await AsyncStorage.removeItem(GUEST_KEY)
}
